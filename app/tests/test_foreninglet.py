"""Tests the ForeningLet API Class"""

from ..foreninglet.api import ForeningLet

def test_api_connection():
    fl_api = ForeningLet()
    response = fl_api.check_api_responds()
    assert response == 200