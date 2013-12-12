import requests
import urlparse

## todo: we need to perform tests with different settings too!
##       how to handle that? (via some method on running_ckan?)


def test_api_readonly(running_ckan):
    """
    Perform some tests, by using the readonly API.
    If everything works correctly, we should only get empty lists
    and 404s, as the database is empty..
    """

    ## site_read
    api_url = urlparse.urljoin(running_ckan.url, '/api/3/action/site_read')
    response = requests.get(api_url)
    assert response.ok
    assert response.status_code == 200
    data = response.json()
    assert data['result'] is True
    assert data['success'] is True

    ## invalid_method_name
    api_url = urlparse.urljoin(
        running_ckan.url, '/api/3/action/invalid_method_name')
    response = requests.get(api_url)
    assert not response.ok
    assert response.status_code == 400
    # data = response.json()  # response is *not* json
    # assert data['result'] is True
    # assert data['success'] is True

    ## package_list
    api_url = urlparse.urljoin(running_ckan.url, '/api/3/action/package_list')
    response = requests.get(api_url)
    assert response.ok
    assert response.status_code == 200
    data = response.json()
    assert data['result'] == []
    assert data['success'] is True

    ## current_package_list_with_resources
    api_url = urlparse.urljoin(
        running_ckan.url, '/api/3/action/current_package_list_with_resources')
    response = requests.get(api_url)
    assert response.ok
    assert response.status_code == 200
    data = response.json()
    assert data['result'] == []
    assert data['success'] is True

    ## revision_list
    api_url = urlparse.urljoin(
        running_ckan.url, '/api/3/action/revision_list')
    response = requests.get(api_url)
    assert response.ok
    assert response.status_code == 200
    data = response.json()
    assert len(data['result']) == 2  # btw, why?
    assert data['success'] is True

    ## package_revision_list
    api_url = urlparse.urljoin(
        running_ckan.url, '/api/3/action/package_revision_list')
    response = requests.get(api_url)
    assert not response.ok
    assert response.status_code == 409  # mumble..
    data = response.json()
    assert 'error' in data
    assert data['success'] is False

    ## package_revision_list?id=invalid
    api_url = urlparse.urljoin(
        running_ckan.url, '/api/3/action/package_revision_list?id=invalid')
    response = requests.get(api_url)
    assert not response.ok
    assert response.status_code == 404
    data = response.json()
    assert 'error' in data
    assert data['success'] is False

    ## related_show
    api_url = urlparse.urljoin(
        running_ckan.url, '/api/3/action/related_show')
    response = requests.get(api_url)
    assert not response.ok
    assert response.status_code == 409  # mumble..
    data = response.json()
    assert 'error' in data
    assert data['success'] is False

    ## related_show?id=invalid
    api_url = urlparse.urljoin(
        running_ckan.url, '/api/3/action/related_show?id=invalid')
    response = requests.get(api_url)
    assert not response.ok
    assert response.status_code == 404
    data = response.json()
    assert 'error' in data
    assert data['success'] is False

    ## related_list
    ## Without arguments, will return an empty list..
    api_url = urlparse.urljoin(
        running_ckan.url, '/api/3/action/related_list')
    response = requests.get(api_url)
    assert response.ok
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True

    ## related_list?id=invalid
    ## With an invalid id, should return 404 (but wouldn't!)
    # api_url = urlparse.urljoin(
    #     running_ckan.url, '/api/3/action/related_list?id=invalid')
    # response = requests.get(api_url)
    # assert not response.ok
    # assert response.status_code == 404
    # data = response.json()
    # assert 'error' in data
    # assert data['success'] is False


def test_api_simple(running_ckan):
    """Base CRUD tests, through the API"""

    DUMMY_API_KEY = 'my-api-key'

    ## Test API (packages list)
    api_url = urlparse.urljoin(running_ckan.url, '/api/3/action/package_list')
    response = requests.get(api_url)
    assert response.ok
    assert response.status_code == 200
    assert response.json()['result'] == []

    ## Create User (we will need this later..)
    running_ckan.paster_with_conf(
        'user', 'add', 'admin', 'password=admin', 'email=admin@example.com',
        'api-key={0}'.format(DUMMY_API_KEY))

    # todo: make sure the user login works correctly
    # todo: create a dataset
    # todo: retrieve it and check that it matches
    # todo: make sure it is listed correctly
    # todo: update the dataset
    # todo: make sure the updates had effect
    # todo: remove the dataset
    # todo: make sure the dataset was deleted correctly
    # todo: get must return 404
    # todo: list must be empty
