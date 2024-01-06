from boto3.session import Session


def create_session(
        region=None, profile=None, *,
        role_arn=None, session=None):
    """
    A handy helper function that will create the
    boto session using our waddle-level settings
    """
    from ..settings import get_region, get_profile, get_role_arn
    if not session:
        profile = profile or get_profile()
        region = region or get_region()
        role_arn = role_arn or get_role_arn()
        session = Session(
            region_name=region,
            profile_name=profile,
        )
        if role_arn:
            sts = session.client('sts')
            response = sts.assume_role(
                RoleArn=role_arn,
                RoleSessionName='waddle')
            creds = response['Credentials']
            session = Session(
                aws_access_key_id=creds['AccessKeyId'],
                aws_secret_access_key=creds['SecretAccessKey'],
                aws_session_token=creds['SessionToken'],
            )
    return session
