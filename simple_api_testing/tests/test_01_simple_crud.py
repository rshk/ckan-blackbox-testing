from .utils import CkanClient


def test_create_package(ckan_env):
    # First, we need to create a user.
    user_data = ckan_env.paster_user_add('api_test', **{
        'password': 'password',
        'email': 'admin@example.com',
    })
    ckan_env.paster_sysadmin_add('api_test')

    API_KEY = user_data['apikey']

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
