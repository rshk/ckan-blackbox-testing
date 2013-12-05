import requests


def test_api_simple(running_ckan):
    response = requests.get(running_ckan)
    assert response.ok
    assert response.status_code == 200
