import pytest

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        
        with app.app_context(): 
            # None
            temp = 1
        yield client

def test_root_endpoint(client):
    '''Test for the / endpoint'''
    rv = client.get('/', follow_redirects=True)
    assert rv.status_code == 200
    assert rv.data != None
