import pytest
from web_app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'uma_chave_secreta_segura'  # Define a secret_key para testes
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Luxury Wheels" in response.data