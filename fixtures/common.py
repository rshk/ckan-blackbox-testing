"""
Common stuff from the fixtures
"""

import os
import subprocess


class CkanInstallation(object):
    def __init__(self, virtualenv, url):
        self.virtualenv = virtualenv
        self.url = url

    @property
    def config_file(self):
        return os.path.join(self.virtualenv, 'etc', 'ckan', 'ckan.ini')

    def python(self, *a):
        return subprocess.check_call((                  # v Mind the comma!
            os.path.join(self.virtualenv, 'bin', 'python'),) + a)

    def paster(self, *a):
        return self.python(os.path.join(self.virtualenv, 'bin', 'paster'), *a)

    def paster_with_conf(self, cmd, *a):
        return self.paster(
            '--plugin=ckan', cmd, '--config={0}'.format(self.config_file), *a)
