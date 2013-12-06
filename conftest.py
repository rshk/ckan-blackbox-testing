import os

if os.environ.get('TRAVIS'):
    from fixtures.ckan_env import *  # noqa
else:
    raise RuntimeError("Unable to figure out which fixtures to load.")
