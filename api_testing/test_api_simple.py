import requests


def test_api_simple(running_ckan):
    """here, we should do some tests on base CRUD"""
    response = requests.get(running_ckan)
    assert response.ok
    assert response.status_code == 200
