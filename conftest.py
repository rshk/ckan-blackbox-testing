import os

if os.environ.get('TRAVIS'):
    from fixtures.ckan_env_travis import *  # noqa
else:
    raise RuntimeError("Unable to figure out which fixtures to load.")
