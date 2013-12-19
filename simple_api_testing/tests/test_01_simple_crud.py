import random

import pytest

from .utils import CkanClient


DUMMY_PACKAGES = {}
DUMMY_PACKAGES['package_0'] = {
    'name': 'hello-dataset',
    'title': 'Hello, dataset!'
}


def get_sysadmin_api_key(ckan_env):
    """Create a sysadmin user, return its API key"""

    user_name = 'api_test_{0:06d}'.format(random.randint(0, 10**6))
    user_data = ckan_env.paster_user_add(user_name, **{
        'password': 'password',
        'email': '{0}@example.com'.format(user_name)})
    ckan_env.paster_sysadmin_add(user_name)
    return user_data['apikey']


@pytest.fixture(params=sorted(DUMMY_PACKAGES.keys()))
def dummy_package(request):
    return DUMMY_PACKAGES[request.param]


def test_simple_package_crud(ckan_env):
    API_KEY = get_sysadmin_api_key(ckan_env)

    with ckan_env.serve() as server:
        client = CkanClient(server.url, api_key=API_KEY)

        # Create a dataset
        # url = urlparse.urljoin(server.url, '/api/3/action/package_create')
        data = {
            'name': 'my-first-dataset',
            'title': 'My First Dataset',
        }
        # response = post_json(url, API_KEY, data)
        response = client.post('/api/3/action/package_create', data=data)
        assert response.ok

        # should be 201 CREATED or 303 FOUND
        assert response.status_code == 200

        data = response.json()
        assert data['success'] is True
        dataset_id = data['result']['id']

        # Get it back
        response = client.get('/api/3/action/package_show?id={0}'
                              .format(dataset_id))
        assert response.ok
        assert response.status_code == 200
        assert data['success'] is True
        assert 'result' in data
        assert data['result']['id'] == dataset_id

        # Delete the dataset
        # url = urlparse.urljoin(server.url, '/api/3/action/package_delete')
        # response = json_request('post', url, API_KEY, {'id': dataset_id})
        response = client.post('/api/3/action/package_delete',
                               data={'id': dataset_id})
        assert response.ok


def test_package_creation(ckan_env, dummy_package):
    """
    Create a dataset, retrieve it and check
    """

    API_KEY = get_sysadmin_api_key(ckan_env)

    with ckan_env.serve() as server:
        client = CkanClient(server.url, api_key=API_KEY)
        response = client.post(
            '/api/3/action/package_create', data=dummy_package)
        assert response.ok

        ## although this should be 201 CREATED or 303 FOUND
        assert response.status_code == 200

        data = response.json()
        assert data['success'] is True
        dataset_id = data['result']['id']

        # Get it back
        response = client.get('/api/3/action/package_show?id={0}'
                              .format(dataset_id))
        assert response.ok
        assert response.status_code == 200
        assert data['success'] is True
        assert 'result' in data
        assert data['result']['id'] == dataset_id

        # # Delete the dataset
        # # url = urlparse.urljoin(server.url, '/api/3/action/package_delete')
        # # response = json_request('post', url, API_KEY, {'id': dataset_id})
        # response = client.post('/api/3/action/package_delete',
        #                        data={'id': dataset_id})
        # assert response.ok
