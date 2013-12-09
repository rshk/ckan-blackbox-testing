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
