import pytest

from ..app import app



def test_root_endpoint(client):
    '''Test for the / endpoint'''
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200

def test_root_endpoint_data(client):
    '''Test for the / endpoint'''
    response = client.get('/', follow_redirects=True)
    assert "Log ind" in str(response.data)
