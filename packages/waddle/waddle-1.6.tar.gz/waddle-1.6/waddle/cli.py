import logging.config
import re
import sys
import click
from murmuration import kms_wrapped
from murmuration import gcm

from .settings import setup_logging
from .param_bunch import ParamBunch
from .yaml_base import KmsWrappedSecret, MasterKeyedSecret
from .utils import long_interactive
from .utils import generate_master_key
from . import version


@click.group(name='waddle')
@click.version_option(version)
def main():
    "cli for managing waddle config files"


def is_secret(key):
    matcher = re.compile('.*(key|secret|token|password).*')
    return matcher.match(key)


@main.command(name='add-secret')
@click.argument('key', metavar='db.password')
@click.option('-f', '--filename', metavar='/path/to/config_file.yml',
              type=click.Path(exists=True), required=True)
def add_secret(filename, key):
    """
    Adds an encrypted secret to the specified configuration file

    Example:
        waddle add-secret -f conf/dev.yml db.password
    """
    setup_logging()
    tty = sys.stdin.isatty()
    log = logging.getLogger(__name__)
    x = ParamBunch()
    x.from_file(
        filename=filename, decrypt=False, handle_tags=False,
        round_trip=True)
    kms_key = x.get('meta.kms_key')
    master_key = None
    try:
        _, _, master_key = x.original_value('meta.master_key')
    except KeyError:
        pass
    if not kms_key and not master_key:
        log.warning('%s needs one of kms_key or master_key.', filename)
        return
    if tty:  # pragma: no cover
        print(f'Enter value for [{key}]: ', end='', file=sys.stderr)
        sys.stderr.flush()
    # stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
    plain_text = sys.stdin.readline().rstrip()
    # plain_text = plain_text.decode('utf-8').rstrip()

    region = x.get('meta.region')
    profile = x.get('meta.profile')
    role_arn = x.get('meta.role_arn')
    if master_key:
        if isinstance(master_key, KmsWrappedSecret):
            master_key = master_key.value
        encrypted_value = gcm.encrypt(plain_text, master_key, 'waddle')
        x[key] = MasterKeyedSecret(encrypted_value)
    else:
        encrypted_value = kms_wrapped.encrypt(
            plain_text, kms_key,
            region, profile, role_arn=role_arn)
        x[key] = KmsWrappedSecret(encrypted_value)
    log.info('saving')
    x.save(filename)
    log.info('done')


@main.command(name='encrypt')
@click.option('-f', '--filename', metavar='/path/to/config_file.yml',
              type=click.Path(exists=True), required=True)
def encrypt(filename):
    """
    Encrypts values for any key that that has the following keywords in it:
      * key
      * password
      * token
      * secret

    Example:
        waddle encrypt -f conf/dev.yml
    """
    setup_logging()
    log = logging.getLogger(__name__)
    x = ParamBunch()
    x.load(filename=filename, decrypt=True, round_trip=True)
    kms_key = x.get('meta.kms_key')
    master_key = None
    try:
        _, _, master_key = x.original_value('meta.master_key')
    except KeyError:
        pass
    if not kms_key and not master_key:
        log.warning('%s needs one of kms_key or master_key.', filename)
        return
    region = x.get('meta.region')
    profile = x.get('meta.profile')
    role_arn = x.get('meta.role_arn')
    values = []
    for key, value in x.items():
        values.append([key, value])
    for key, value in values:
        if is_secret(key) and not key.startswith('meta.'):
            if master_key:
                if isinstance(master_key, KmsWrappedSecret):
                    master_key = master_key.value
                encrypted_value = gcm.encrypt(value, master_key, 'waddle')
                x[key] = MasterKeyedSecret(encrypted_value)
            else:
                encrypted_value = kms_wrapped.encrypt(
                    value, kms_key, region=region, profile=profile,
                    role_arn=role_arn)
                x[key] = KmsWrappedSecret(encrypted_value)
    x.save(filename)


@main.command(name='deploy')
@click.option('-f', '--filename', metavar='/path/to/config_file.yml',
              type=click.Path(exists=True), required=True)
@click.option('-e', '--encrypted', is_flag=True)
def deploy(filename, encrypted):
    """
    Deploys a locally stored config file to aws:

    Example:
        waddle deploy -f conf/dev.yml

    Use the --encrypt flag to push all values as kms encrypted to
    parameter store.
    """
    x = ParamBunch(filename=filename)
    x.to_aws(force_encryption=encrypted)


@main.command(name='undeploy')
@click.option('-f', '--filename', metavar='/path/to/config_file.yml',
              type=click.Path(exists=True), required=True)
def undeploy(filename):
    """
    Deploys a locally stored config file to aws:

    Example:
        waddle deploy -f conf/dev.yml
    """
    x = ParamBunch(filename=filename)
    x.delete_from_aws()


@main.command(name='add_master_key')
@click.option('-f', '--filename', metavar='/path/to/config_file.yml',
              type=click.Path(exists=True), required=True)
@click.option('-r', '--reencrypt', is_flag=True, show_default=True,
              default=False, help='will reencrypt all secrets with the added '
                                  'master key')
def add_master_key(filename, reencrypt):
    """
    adds a master key to the specified config file.
    """
    setup_logging()
    log = logging.getLogger(__name__)
    x = ParamBunch(filename=filename, round_trip=True)
    kms_key = x.get('meta.kms_key')
    if not kms_key:
        log.warning('%s needs a kms_key.', filename)
        return
    try:
        _, _, master_key = x.original_value('meta.master_key')
    except KeyError:
        master_key = None
    if master_key:
        log.info('rotating existing master key')
        reencrypt = True
    region = x.get('meta.region')
    profile = x.get('meta.profile')
    role_arn = x.get('meta.role_arn')
    new_master_key = generate_master_key()
    if reencrypt:
        for key in x.encrypted:
            with long_interactive('encrypting', key=key) as ctx:
                value = x.get(key)
                encrypted_value = gcm.encrypt(value, new_master_key, 'waddle')
                x[key] = MasterKeyedSecret(encrypted_value)
                ctx.succeeded()
    with long_interactive('saving', key=filename) as ctx:
        encrypted_value = kms_wrapped.encrypt(
            new_master_key, alias=kms_key, profile=profile, region=region,
            role_arn=role_arn)
        x.meta.master_key = KmsWrappedSecret(encrypted_value)
        x.save(filename)
        ctx.succeeded()


if __name__ == "__main__":
    main()
