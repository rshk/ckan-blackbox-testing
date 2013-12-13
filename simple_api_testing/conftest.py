import os
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


@pytest.fixture
def ckan_url():
    base_url = os.environ.get('CKAN_URL', 'http://127.0.0.1:5000')

    def get_ckan_url(path):
        return urlparse.urljoin(base_url, path)

    return get_ckan_url


@pytest.fixture
def api_key():
    return os.environ.get('API_KEY', 'my-api-key')
