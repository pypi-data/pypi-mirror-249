from collections.abc import Mapping
import logging
import os
import re

from ruamel.yaml.comments import CommentedMap
from murmuration import kms_wrapped
from .bunch import Bunch
from .aws import yield_parameters
from .aws import put_parameter
from .aws import delete_parameters
from .aws import ssm_key
from .aws import create_session, create_ssm_client, create_kms_client
from .yaml_base import Yaml, dump_yaml
from .yaml_base import SsmValue, KmsWrappedSecret, MasterKeyedSecret
from .yaml_base import load_yaml_basic, reset_special_value_clients


__all__ = [
    'ParamBunch',
]


dict_class = CommentedMap


class ParamBunch(Bunch):
    def __init__(self, values=None, prefix=None, filename=None, round_trip=False):
        super().__init__(values)
        super()._set('original_values', values)
        super()._set('encrypted', [])
        super()._set('spinner', None)
        if prefix or filename:
            self.load(prefix=prefix, filename=filename, round_trip=round_trip)

    def _is_reserved(self, key):
        if key in [ 'values', 'original_value', 'encrypted', 'spinner', ]:
            return True
        return key in self.__dict__ and not key.startswith('__')

    def aws_items(self, values=None, prefix=None):
        prefix = prefix or [ '', self.meta.namespace ]
        for key, value in self.items(values, prefix):
            if '.meta.' in key:
                continue
            key = key.replace('.', '/')
            yield key, value

    def file_items(self, values=None, prefix=None):
        meta_prefix = re.compile(r'^\.?meta\.')
        for key, value in self.items(values, prefix):
            if meta_prefix.match(key):
                continue
            yield key, value
        yield from self.items(values=self.meta.values, prefix=[ 'meta' ])

    def to_dict(self):
        result = super().to_dict()
        return result

    @staticmethod
    def _traverse(d, prefix=None):
        prefix = prefix or []
        for key, value in d.items():
            if isinstance(value, Mapping):
                yield from ParamBunch._traverse(value, prefix + [ key ])
            else:
                yield '.'.join(prefix + [ key ]), value

    @staticmethod
    def try_decrypt(
            value, region=None, profile=None,
            session=None, client=None):
        # an artifact of murmuration encryption is that all
        # encrypted values will start with 'AQI', so fast fail
        # out of decrypt
        if isinstance(value, str) and value[:3] == 'AQI':
            try:
                value = kms_wrapped.decrypt(
                    value, region, profile, session, client=client)
            except ValueError:
                pass
        return value

    @classmethod
    def get_master_key(cls, meta, profile, region, role_arn, kms_key):
        master_key = meta.get('master_key')
        if isinstance(master_key, KmsWrappedSecret):
            master_key.profile = profile
            master_key.region = region
            master_key.role_arn = role_arn
            master_key.kms_key = kms_key
            return master_key
        return master_key

    def from_file(  # pylint: disable=unused-argument
            self, filename,
            decrypt=True,
            round_trip=False, **kwargs):
        # late load logger in case anyone sets up logging
        # later
        log = logging.getLogger(__name__)
        if not os.path.exists(filename):
            log.warning('waddle: could not find %s', filename)
            return

        special_values, master_key = [], None
        if round_trip:
            with open(filename, 'r', encoding='utf-8') as f:
                y = Yaml()
                data = y.load(f)
        else:
            data, master_key, special_values = load_yaml_basic(filename)
        meta = data.get('meta', {})
        region = meta.get('region')
        profile = meta.get('profile')
        kms_key = meta.get('kms_key')
        role_arn = meta.get('role_arn')
        if round_trip:
            master_key = self.get_master_key(
                meta, profile, region, role_arn, kms_key)
            special_values = y.special_values
        reset_special_value_clients(
            special_values, profile=profile, region=region,
            role_arn=role_arn, master_key=master_key)
        super()._set('original_values', data)
        values = []
        for key, value in ParamBunch._traverse(data):
            if self._is_reserved(key):
                raise KeyError(f'`{key}` is not a valid key name')
            if key.startswith('meta.'):
                self[key] = value
            else:
                values.append((key, value))
        self.handle_file_values(values, decrypt)

    def handle_file_values(self, values, decrypt, session=None, client=None):
        from murmuration.aws import kms_client
        region = self.get('meta.region')
        profile = self.get('meta.profile')
        client = kms_client(
            region=region, profile=profile,
            session=session, client=client)
        for key, value in values:
            if not decrypt:
                self[key] = value
                continue
            new_value = self[key] = ParamBunch.try_decrypt(
                value, region, profile,
                session=session, client=client)
            tagged_classes = (SsmValue, KmsWrappedSecret, MasterKeyedSecret)
            tagged_value = isinstance(value, tagged_classes)
            if new_value != value or tagged_value:
                self.encrypted.append(key)

    def load(self, prefix=None, filename=None, decrypt=True, round_trip=False):
        if prefix:
            self.from_aws(prefix)
        if filename:
            self.from_file(filename, decrypt, round_trip)

    def from_aws(self, prefix):
        if not prefix.startswith('/'):
            prefix = f'/{prefix}'
        prefix = prefix.replace('.', '/')
        for key, value, type_ in yield_parameters(prefix):
            if type_ == 'SecureString':
                self.encrypted.append(key)
            elif type_ == 'StringList':
                value = value.split(',')
            self[key] = value
        self.meta.namespace = prefix[1:].replace('/', '.')

    def _encrypted_keys(self):
        namespace = self.get('meta.namespace', '')
        ms_encrypted = set()
        for x in self.encrypted:
            ms_encrypted.add(ssm_key(namespace, x))
        return ms_encrypted

    def to_aws(
            self, force_encryption=False, verbose=True,
            profile=None, region=None,
            role_arn=None, session=None, ssm_client=None):
        from .aws.pstore import create_ssm_client
        ssm_client = create_ssm_client(
            profile=profile, region=region, role_arn=role_arn,
            session=session, client=ssm_client)
        ms_encrypted = self._encrypted_keys()
        kms_key = self.get('meta.kms_key')
        for key, value in self.aws_items():
            encrypted = key in ms_encrypted
            encrypted = encrypted or force_encryption
            put_parameter(
                key, value, kms_key, encrypted, verbose,
                session=session, client=ssm_client)

    def delete_from_aws(
            self, verbose=True,
            profile=None, region=None, role_arn=None,
            session=None, ssm_client=None):
        from .aws.pstore import create_ssm_client
        ssm_client = create_ssm_client(
            profile=profile, region=region, role_arn=role_arn,
            session=session, client=ssm_client)
        keys = [ key for key, _ in self.aws_items() ]
        delete_parameters(
            *keys, verbose=verbose,
            session=session, client=ssm_client)

    def original_value(self, key):
        data = self.original_values
        if key in data:
            return data, key, data[key]
        pieces = key.split('.')
        for x in pieces[:-1]:
            data = data[x]
        key = pieces[-1]
        return data, key, data[key]

    def original_parent(self, key):
        data = self.original_values
        pieces = key.split('.')
        try:
            for x in pieces[:-1]:
                data = data[x]
            return data, pieces[-1]
        except (KeyError, TypeError):
            return self.original_values, key

    def fill_back(self):
        updated_values = []
        new_values = []
        for key, value in self.items():
            try:
                parent, key, original_value = self.original_value(key)
                if value != original_value:
                    updated_values.append((parent, key, value))
            except (KeyError, TypeError):
                new_values.append((key, value))
        self.handle_updates(updated_values)
        self.handle_new(new_values)

    def handle_updates(self, updated_values):
        # pylint: disable=access-member-before-definition
        for parent, key, value in updated_values:
            parent[key] = value
        if self.original_values is None:
            self.original_values = dict_class()

    def handle_new(self, new_values):
        for key, value in new_values:
            parent, x = self.original_parent(key)
            parent[x] = value

    def save(self, filename):
        log = logging.getLogger(__name__)
        self.fill_back()
        dump_yaml(self.original_values, filename)
