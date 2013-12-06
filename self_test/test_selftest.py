"""
Self-test for the blackbox testing..
"""

import requests
import urlparse


def test_api_simple(running_ckan):
    ## Test Web UI (homepage)
    response = requests.get(running_ckan)
    assert response.ok
    assert response.status_code == 200

    ## Test API (packages list)
    api_url = urlparse.urljoin(running_ckan, '/api/3/action/package_list')
    response = requests.get(api_url)
    assert response.ok
    assert response.status_code == 200
    assert response.json()['result'] == []
