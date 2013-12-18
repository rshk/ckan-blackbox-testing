import json
import requests
import urlparse


def json_request(method, url, api_key, data, **other):
    data = json.dumps(data)
    if 'headers' not in other:
        other['headers'] = {}
    other['headers']['Authorization'] = api_key
    other['headers']['Content-type'] = 'application/json'
    return requests.request(method, url, data=data, **other)


def post_json(url, api_key, data, **other):
    return json_request('post', url, api_key, data, **other)


def test_create_package(ckan_env):
    # First, we need to create a user.
    user_data = ckan_env.paster_user_add('api_test', **{
        'password': 'password',
        'email': 'admin@example.com',
    })
    ckan_env.paster_sysadmin_add('api_test')

    API_KEY = user_data['apikey']

    with ckan_env.serve() as server:
        # Create a dataset
        url = urlparse.urljoin(server.url, '/api/3/action/package_create')
        data = {
            'name': 'my-first-dataset',
            'title': 'My First Dataset',
        }
        response = post_json(url, API_KEY, data)
        assert response.ok

        # should be 201 CREATED or 303 FOUND
        assert response.status_code == 200

        data = response.json()
        assert data['success'] is True
        dataset_id = data['result']['id']

        # Get it back
        url = urlparse.urljoin(
            server.url, '/api/3/action/package_show?id={0}'.format(dataset_id))
        response = requests.get(url)
        assert response.ok
        assert response.status_code == 200
        assert data['success'] is True
        assert 'result' in data
        assert data['result']['id'] == dataset_id

        # Delete the dataset
        url = urlparse.urljoin(server.url, '/api/3/action/package_delete')
        response = json_request('post', url, API_KEY, {'id': dataset_id})
        assert response.ok
