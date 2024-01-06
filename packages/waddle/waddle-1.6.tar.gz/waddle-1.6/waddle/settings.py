import logging


# settings to control aws connection
aws_profile = None
aws_secret_access_key = None
aws_access_key_id = None
aws_region = None
aws_role_arn = None
verbose_mode = False
test_mode = False


def set_profile(profile):
    global aws_profile
    aws_profile = profile


def get_profile():
    return aws_profile


def set_region(region):
    global aws_region
    aws_region = region


def get_region():
    return aws_region


def set_role_arn(role_arn):
    global aws_role_arn
    aws_role_arn = role_arn


def get_role_arn():
    return aws_role_arn


def set_verbose_mode():
    return verbose_mode


def get_verbose_mode():
    return verbose_mode


def setup_logging():
    if test_mode:
        return
    logging.config.dictConfig({
        'version': 1,
        'root': {
            'handlers': ['waddle'],
            'level': 'INFO',
        },
        'handlers': {
            'waddle': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'waddle',
            }
        },
        'formatters': {
            'waddle': {
                'format': '[{asctime}.{msecs:03.0f}] [{name}] {message}',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'style': '{',
            },
        },
    })


def get_test_mode():
    return test_mode


def set_test_mode(boo):
    global test_mode
    test_mode = boo
