import os
import urlparse

import pytest
import requests


@pytest.fixture
def ckan_url():
    base_url = os.environ.get('CKAN_URL', 'http://127.0.0.1:5000')

    def get_ckan_url(path):
        return urlparse.urljoin(base_url, path)

    return get_ckan_url


def test_site_read(ckan_url):
    api_url = ckan_url('/api/3/action/site_read')
    response = requests.get(api_url)
    assert response.ok
    assert response.status_code == 200
    data = response.json()
    assert data['result'] is True
    assert data['success'] is True


def test_invalid_method_name(ckan_url):
    ## invalid_method_name
    api_url = ckan_url('/api/3/action/invalid_method_name')
    response = requests.get(api_url)
    assert not response.ok
    assert response.status_code == 400
    # data = response.json()  # response is *not* json
    # assert data['result'] is True
    # assert data['success'] is True

    # ## package_list
    # api_url = urlparse.urljoin(running_ckan.url, '/api/3/action/package_list')
    # response = requests.get(api_url)
    # assert response.ok
    # assert response.status_code == 200
    # data = response.json()
    # assert data['result'] == []
    # assert data['success'] is True

    # ## current_package_list_with_resources
    # api_url = urlparse.urljoin(
    #     running_ckan.url, '/api/3/action/current_package_list_with_resources')
    # response = requests.get(api_url)
    # assert response.ok
    # assert response.status_code == 200
    # data = response.json()
    # assert data['result'] == []
    # assert data['success'] is True

    # ## revision_list
    # api_url = urlparse.urljoin(
    #     running_ckan.url, '/api/3/action/revision_list')
    # response = requests.get(api_url)
    # assert response.ok
    # assert response.status_code == 200
    # data = response.json()
    # assert len(data['result']) == 2  # btw, why?
    # assert data['success'] is True

    # ## package_revision_list
    # api_url = urlparse.urljoin(
    #     running_ckan.url, '/api/3/action/package_revision_list')
    # response = requests.get(api_url)
    # assert not response.ok
    # assert response.status_code == 409  # mumble..
    # data = response.json()
    # assert 'error' in data
    # assert data['success'] is False

    # ## package_revision_list?id=invalid
    # api_url = urlparse.urljoin(
    #     running_ckan.url, '/api/3/action/package_revision_list?id=invalid')
    # response = requests.get(api_url)
    # assert not response.ok
    # assert response.status_code == 404
    # data = response.json()
    # assert 'error' in data
    # assert data['success'] is False

    # ## related_show
    # api_url = urlparse.urljoin(
    #     running_ckan.url, '/api/3/action/related_show')
    # response = requests.get(api_url)
    # assert not response.ok
    # assert response.status_code == 409  # mumble..
    # data = response.json()
    # assert 'error' in data
    # assert data['success'] is False

    # ## related_show?id=invalid
    # api_url = urlparse.urljoin(
    #     running_ckan.url, '/api/3/action/related_show?id=invalid')
    # response = requests.get(api_url)
    # assert not response.ok
    # assert response.status_code == 404
    # data = response.json()
    # assert 'error' in data
    # assert data['success'] is False

    # ## related_list
    # ## Without arguments, will return an empty list..
    # api_url = urlparse.urljoin(
    #     running_ckan.url, '/api/3/action/related_list')
    # response = requests.get(api_url)
    # assert response.ok
    # assert response.status_code == 200
    # data = response.json()
    # assert data['success'] is True

    # ## related_list?id=invalid
    # ## With an invalid id, should return 404 (but wouldn't!)
    # # api_url = urlparse.urljoin(
    # #     running_ckan.url, '/api/3/action/related_list?id=invalid')
    # # response = requests.get(api_url)
    # # assert not response.ok
    # # assert response.status_code == 404
    # # data = response.json()
    # # assert 'error' in data
    # # assert data['success'] is False
