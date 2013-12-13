import os
import subprocess
import time
import urlparse

import pytest

HERE = os.path.abspath(os.path.dirname(__file__))


## Paster command to create users:
# paster --plugin=ckan user --config=$VIRTUAL_ENV/etc/ckan/production.ini
# add admin password=admin email=admin@example.com api-key=my-api-key

## Paster command to initialize database
# paster --plugin=ckan db --config=$VIRTUAL_ENV/etc/ckan.ini init

## Paster command to rebuild search index
# paster --plugin=ckan search-index --config=$VIRTUAL_ENV/etc/ckan.ini rebuild

## Paster command to run server
# paster --plugin=ckan serve $VIRTUAL_ENV/etc/ckan.ini


class CkanEnvironment(object):
    def __init__(self, venv_root):
        self.venv_root = venv_root
        #self.postgresql_url = postgresql_url
        #self.solr_url = solr_url

        ## todo: we'd also need a way to recreate database!
        ## maybe, let's ask admin credentials for postgres?

    @classmethod
    def from_environment(cls):
        venv_root = os.environ['CKAN_VIRTUALENV']
        # postgresql_url = os.environ['CKAN_POSTGRESQL_URL']
        # solr_url = os.environ['CKAN_SOLR_URL']
        return cls(venv_root)

    @classmethod
    def get_ephemeral_port(cls):
        """Ugly hack to allocate an ephemeral port"""

        import socket
        sock = socket.socket(socket.AF_INET)
        sock.bind(('127.0.0.1', 0))
        addr, port = sock.getsockname()
        sock.close()
        return port

    @property
    def conf_file_path(self):
        return os.path.join(self.venv_root, 'etc', 'ckan.ini')

    def run_paster(self, *args):
        python = os.path.join(self.venv_root, 'bin', 'python')
        paster = os.path.join(self.venv_root, 'bin', 'paster')
        return subprocess.check_call([python, paster] + args)

    def run_paster_with_conf(self, command, *args):
        return self.run_paster(
            command, '--config={0}'.format(self.conf_file_path), *args)

    def serve(self):
        python = os.path.join(self.venv_root, 'bin', 'python')
        paster = os.path.join(self.venv_root, 'bin', 'paster')

        # todo: we might want to copy the configuration file, so we
        # can safely alter some configuration values (such as port)?
        return CkanServerWrapper([
            python, paster, 'serve', self.conf_file_path
        ], url='http://127.0.0.1:5000')


class CkanServerWrapper(object):
    def __init__(self, args, url):
        self.args = args
        self.url = url

    def start(self):
        self.process = subprocess.Popen(self.args)
        time.sleep(1)
        return self.process

    def stop(self):
        self.process.terminate()
        self.process.wait()

    def __enter__(self):
        return self.start()

    def __exit__(self, e_type, exc, tb):
        self.stop()


@pytest.fixture(scope='session')
def ckan_env():
    return CkanEnvironment.from_environment()


@pytest.fixture(scope='module')
def ckan_url(request, ckan_env):
    server = ckan_env.serve()

    def finalize():
        server.stop()
    request.addfinalizer(finalize)

    base_url = server.url

    def get_ckan_url(path):
        return urlparse.urljoin(base_url, path)

    server.start()

    return get_ckan_url


@pytest.fixture
def api_key():
    return os.environ.get('API_KEY', 'my-api-key')
