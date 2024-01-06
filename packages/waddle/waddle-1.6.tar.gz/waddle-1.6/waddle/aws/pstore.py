from contextlib import nullcontext
from typing import Generator, Tuple
from murmuration.helpers import prefix_alias


__all__ = [
    'yield_parameters',
    'put_parameter',
    'get_parameter',
    'delete_parameters',
    'waddle_key',
    'ssm_key',
    'create_ssm_client',
    'create_kms_client',
]

StrTuple = Tuple[str, str, str]


def waddle_key(prefix, key):
    return key.replace(prefix, '').replace('/', '.')[1:]


def ssm_key(prefix, key):
    prefix = f'/{prefix}' if prefix else ''
    return f'{prefix}/{key}'.replace('.', '/')


def create_kms_client(
        profile=None, region=None, *,
        role_arn=None, session=None, client=None,):
    from .session import create_session
    if client:
        return client
    session = create_session(
        profile=profile,
        region=region,
        role_arn=role_arn,
        session=session)
    return session.client('kms')


def create_ssm_client(
        profile=None, region=None, *,
        role_arn=None, session=None, client=None):
    from .session import create_session
    if client:
        return client
    session = create_session(
        profile=profile,
        region=region,
        role_arn=role_arn,
        session=session)
    return session.client('ssm')


def get_parameter(key, profile=None, region=None, session=None, client=None):
    ssm = create_ssm_client(
        profile=profile, region=region, session=session, client=client)
    try:
        result = ssm.get_parameter(Name=key, WithDecryption=True)
        return result['Parameter']['Value']
    except:  # noqa, pylint: disable=bare-except
        return None


def put_parameter(
        key, value, kms_key, encrypted, verbose=False,
        region=None, profile=None, session=None, client=None):
    from ..utils import long_interactive
    ctx = nullcontext()
    if verbose:
        ctx = long_interactive('pushing', key, encrypted)
    with ctx:
        ssm = create_ssm_client(
            region=region, profile=profile,
            session=session, client=client)
        params = {}
        if isinstance(value, list):
            value = ','.join([ f'{x}' for x in value ])
            params['Type'] = 'StringList'
        elif encrypted:
            params['Type'] = 'SecureString'
            if kms_key:
                params['KeyId'] = prefix_alias(kms_key)
        else:
            params['Type'] = 'String'
        result = ssm.put_parameter(
            Name=key,
            Value=value,
            Overwrite=True,
            **params)
        if verbose:
            ctx.succeeded()
    return result


def delete_parameters(*keys, verbose=False, region=None, profile=None,
                      session=None, client=None):
    from ..utils import long_interactive
    ssm = create_ssm_client(
        region=region, profile=profile, session=session, client=client)
    n_start = 1
    while keys:
        rg = keys[:10]
        ctx = nullcontext()
        if verbose:
            message = f'{n_start}=>{n_start + len(rg) - 1}'
            ctx = long_interactive('deleting keys', message)
        with ctx:
            ssm.delete_parameters(Names=rg)
            keys = keys[10:]
            n_start += len(rg)
            if verbose:
                ctx.succeeded()


def yield_parameters(
        prefix, decrypt=True,
        profile=None, region=None, session=None,
        client=None) -> Generator[StrTuple, None, None]:
    ssm = create_ssm_client(
        profile=profile, region=region, session=session, client=client)
    paginator = ssm.get_paginator('get_parameters_by_path')
    for page in paginator.paginate(
            Path=prefix,
            Recursive=True,
            WithDecryption=decrypt,
            PaginationConfig={
                'PageSize': 10,
            }):
        for x in page['Parameters']:
            key = x['Name']
            value = x['Value']
            key = waddle_key(prefix, key)
            yield key, value, x['Type']
