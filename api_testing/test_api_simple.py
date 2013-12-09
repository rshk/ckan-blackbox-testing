import requests
import urlparse


def test_api_simple(running_ckan):
    """Base CRUD tests, through the API"""

    ## Test API (packages list)
    api_url = urlparse.urljoin(running_ckan.url, '/api/3/action/package_list')
    response = requests.get(api_url)
    assert response.ok
    assert response.status_code == 200
    assert response.json()['result'] == []

    ## Create User (we will need this later..)
    running_ckan.paster_with_conf(
        'user', 'add', 'admin', 'password=admin', 'email=admin@example.com',
        'api-key=my-api-key')

    # todo: create a dataset
    # todo: retrieve it and check that it matches
    # todo: make sure it is listed correctly
    # todo: update the dataset
    # todo: make sure the updates had effect
    # todo: remove the dataset
    # todo: make sure the dataset was deleted correctly
    # todo: get must return 404
    # todo: list must be empty
