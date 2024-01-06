import os
import random
import sys


__all__ = [
    'load_config',
    'start_notification',
    'end_notification',
    'long_interactive',
    'generate_master_key',
]


def load_config(*filenames, decrypt=True):
    """
    Loads the specified config files if they exist in the order
    specified.  This is useful for having "cascading" configs
    and also for suppressing warnings from `ParamBunch.from_file`
    """
    from .param_bunch import ParamBunch
    conf = ParamBunch()
    for x in filenames:
        if os.path.exists(x):
            conf.from_file(x, decrypt=decrypt)
    return conf


def start_notification(action, key, encrypted=False):
    from halo import Halo
    encrypted = ' (encrypted)' if encrypted else ''
    if sys.stdout.isatty():  # pragma: no cover
        spinner = Halo(f'{action} {key}{encrypted}', spinner='dots')
        spinner.start()
        return spinner
    message = f'{action} {key}{encrypted} ....'
    print(message, end='')
    return None


SUCCESS = '\N{heavy check mark}\N{vs16}'
FAILURE = '\N{ballot x}\N{vs16}'


def end_notification(spinner, success=True):
    from halo.halo import colored_frame
    mark = SUCCESS if success else FAILURE
    if sys.stdout.isatty():  # pragma: no-cover
        if success:
            spinner.succeed()
        else:
            mark = colored_frame(mark, 'red')
            spinner.stop_and_persist(mark)
    else:
        print(mark, end='')


class long_interactive:
    def __init__(self, action, key, encrypted=False):
        self.spinners = []
        self.action = action
        self.key = key
        self.encrypted = encrypted
        self.success = None

    def succeeded(self):
        self.success = True

    def failed(self):
        self.success = False

    def __enter__(self):
        spinner = start_notification(self.action, self.key, self.encrypted)
        self.spinners.append(spinner)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        spinner = self.spinners.pop()
        end_notification(spinner, self.success)


def generate_master_key(length=32):
    chars = (
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '_+-/;,.=~!@#$%^&*'
    )
    rg = [ random.choice(chars) for _ in range(length) ]
    return ''.join(rg)
