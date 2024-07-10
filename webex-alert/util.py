from functools import wraps
from inspect import getfullargspec
import logging
import os

script_dir = os.path.dirname(__file__)
root_dir = os.path.join(script_dir, "..")

def log_method(method):

    argspec = getfullargspec(method)
    hide = []
    if "accesstoken" in argspec.args:
        hide.append(argspec.args.index("accesstoken"))
    if "refreshtoken" in argspec.args:
        hide.append(argspec.args.index("refreshtoken"))
        
    @wraps(method)
    def wrapper(*args, **kwargs):
        display_args = [args[i] if i not in hide else "SECRET" for i in range(len(args))]
        logger = logging.getLogger("webex-alert")
        fn = os.path.basename(method.__globals__['__file__'])
        logger.debug(f"Call to {fn}->{method.__name__} with params {display_args}")
        return method(*args, **kwargs)
    
    return wrapper