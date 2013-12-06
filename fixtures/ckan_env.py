import os
import random
import shutil
import subprocess
import sys
import tempfile
import time

import pytest


HERE = os.path.abspath(os.path.dirname(__file__))

JETTY_CONF = """\
NO_START=0
JETTY_HOST=127.0.0.1
JETTY_PORT=8983
JAVA_HOME={java}
""".format(java=os.environ.get('JAVA_HOME', ''))

with open(os.path.join(HERE, 'data', 'ckan.ini')) as f:
    CKAN_CONF = f.read()


@pytest.fixture(scope='module')
def cleandir(request):
    tmpdir = tempfile.mkdtemp()

    def cleanup():
        shutil.rmtree(tmpdir)
    request.addfinalizer(cleanup)

    return tmpdir


@pytest.fixture(scope='module')
def virtualenv(request, cleandir):
    """Returns path to a fresh virtualenv, created using the current Python"""

    os.chdir(cleandir)
    venv_root = os.path.join(cleandir, 'venv')
    subprocess.check_call([
        'virtualenv', '--python', sys.executable, venv_root])
    assert os.path.exists(os.path.join(venv_root, 'bin', 'python'))
    assert os.path.exists(os.path.join(venv_root, 'bin', 'pip'))

    def cleanup():
        shutil.rmtree(venv_root)
    request.addfinalizer(cleanup)

    return venv_root


@pytest.fixture(scope='module')
def clean_database(request):
    """Returns URL to a clean PostgreSQL database"""

    db_data = {
        "host": 'localhost',
        "port": '5432',
        "name": 'ckan_{0:06d}'.format(random.randint(0, 10 ** 6)),
        "username": 'ckan',
        "password": 'ckan',
    }

    subprocess.check_call([
        'sudo', '-u', 'postgres', 'psql', '-c',
        "CREATE USER {username} WITH PASSWORD '{password}';".format(**db_data)
    ])
    subprocess.check_call([
        'sudo', '-u', 'postgres',  # 'psql', '-c',
        #"CREATE DATABASE {name} WITH OWNER {username};".format(**db_data)
        'createdb', '-E', 'utf-8', '-O', db_data['username'], db_data['name'],
    ])

    def cleanup():
        subprocess.check_call([
            'sudo', '-u', 'postgres', 'dropdb', db_data['name'],
        ])
        subprocess.check_call([
            'sudo', '-u', 'postgres', 'dropuser', db_data['username'],
        ])
    request.addfinalizer(cleanup)

    return "postgresql://{username}:{password}@{host}:{port}/{name}"\
        "".format(**db_data)


@pytest.fixture(scope='module')
def clean_solr_index(request):
    """Returns URL to a clean Solr index"""

    subprocess.check_call([
        'sudo', 'apt-get', 'install', 'solr-jetty',
    ])
    with open('/tmp/jetty-conf.txt', 'w') as f:
        f.write(JETTY_CONF)
    subprocess.check_call([
        'sudo', 'cp', '/tmp/jetty-conf.txt', '/etc/default/jetty',
    ])

    ## todo: If we're on debian, we need to fix a broken link too..
    # rm /var/lib/jetty/webapps/solr
    # ln -s /usr/share/solr/web/ /var/lib/jetty/webapps/solr

    ckan_schema = os.path.join(HERE, 'data', 'ckan-schema-2.0.xml')
    subprocess.check_call([
        'sudo', 'cp', ckan_schema, '/etc/solr/conf/schema.xml',
    ])

    subprocess.check_call([
        'sudo', 'service', 'jetty', 'restart',
    ])

    def cleanup():
        ## Empty /var/lib/solr/data
        subprocess.check_call(['sudo', 'service', 'jetty', 'stop'])
        subprocess.check_call(['sudo', 'rm', '-rfv', '/var/lib/solr/data'])
        subprocess.check_call(['sudo', 'mkdir', '-p', '/var/lib/solr/data'])
        subprocess.check_call(['sudo', 'chown', '-R', 'jetty:jetty',
                               '/var/lib/solr/data'])
        subprocess.check_call(['sudo', 'chmod', '750', '/var/lib/solr/data'])
    request.addfinalizer(cleanup)

    return "http://127.0.0.1:8983/solr"


@pytest.fixture(scope='module')
def ckan_installation(virtualenv, clean_database, clean_solr_index):
    context = {
        'venv': virtualenv,
        'db_url': clean_database,
        'solr_url': clean_solr_index,
        'datadir': os.path.join(virtualenv, 'data'),
        'confdir': os.path.join(virtualenv, 'etc', 'ckan'),
    }
    os.makedirs(context['datadir'])
    os.makedirs(context['confdir'])

    ckan_conf_file = os.path.join(context['confdir'], 'ckan.ini')

    with open(ckan_conf_file, 'w') as f:
        f.write(CKAN_CONF.format(**context))

    with open(os.path.join(HERE, 'data', 'who.ini'), 'r') as f:
        WHO_INI = f.read()

    with open(os.path.join(context['confdir'], 'who.ini'), 'w') as f:
        f.write(WHO_INI)

    ## Ok, now we can install stuff..
    sources_dir = os.path.join(virtualenv, 'src')
    ckan_dir = os.path.join(sources_dir, 'ckan')
    os.makedirs(sources_dir)
    subprocess.check_call([
        'git', 'clone', 'https://github.com/okfn/ckan', ckan_dir])

    os.chdir(ckan_dir)

    PIP = os.path.join(virtualenv, 'bin', 'pip')
    PYTHON = os.path.join(virtualenv, 'bin', 'python')

    assert os.path.exists(PIP)
    assert os.path.exists(PYTHON)

    subprocess.check_call([
        PIP, 'install', '-r', os.path.join(ckan_dir, 'requirements.txt')
    ])

    subprocess.check_call([PYTHON, 'setup.py', 'install'])

    PASTER = os.path.join(virtualenv, 'bin', 'paster')
    subprocess.check_call([PASTER, 'db', '--conf', ckan_conf_file, 'init'])

    return virtualenv


@pytest.fixture(scope='module')
def running_ckan(request, ckan_installation):
    PASTER = os.path.join(ckan_installation, 'bin', 'paster')
    ckan_conf_file = os.path.join(ckan_installation, 'etc', 'ckan', 'ckan.ini')
    proc = subprocess.Popen([PASTER, 'serve', ckan_conf_file])

    def cleanup():
        proc.terminate()

    request.addfinalizer(cleanup)

    time.sleep(5)  # allow some time from coming up
    return 'http://localhost:5000'
