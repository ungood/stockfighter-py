import glob
import logging
from os import path
import sys

logger = logging.getLogger(__name__)

__all__ = []
levels = {}

basedir = path.dirname(__file__)
for name in glob.glob(path.join(basedir, '*.py')):
    level_name = path.splitext(path.split(name)[-1])[0]
    if not level_name.startswith('_'):
        module_name = "{}.{}".format(__name__, level_name)
        logger.debug("Importing module '%s'.", module_name)
        try:
            module = __import__(module_name)
            __all__.append(level_name)
            levels[level_name] = sys.modules[module_name]
        except:
            logger.exception('Caught exception while loading the %r plug-in.', module_name)

__all__.sort()

def solve(level_name, client, level_info):
    levels[level_name].solve(client, level_info)