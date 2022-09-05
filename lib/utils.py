import platform

from constants import VERBOSE_LOGGING

def is_windows():
    return platform.system() == 'Windows'

def is_mac():
    return platform.system() == 'Darwin'

def logger(message, verbose=VERBOSE_LOGGING):
    if verbose:
        print(message)