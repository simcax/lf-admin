import pytest

def test_init():
    # Let's just try an import the app
    from app import app
    assert app is not None
