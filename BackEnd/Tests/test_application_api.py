import pytest
import sys
import os
import json

# Add BackEnd folder to path so we can import application.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import application as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'OK'

def test_current_user(client):
    response = client.get('/api/current-user')
    assert response.status_code == 200
    assert 'username' in response.json

def test_register_missing_fields(client):
    response = client.post('/api/register', json={})
    assert response.status_code == 400

def test_login_missing_fields(client):
    response = client.post('/api/login', json={})
    assert response.status_code == 400

def test_details_not_found(client):
    response = client.get('/details/fake-id')
    assert response.status_code == 404
    assert 'Course not found' in response.get_data(as_text=True)

def test_get_columns(client):
    response = client.get('/api/columns')
    assert response.status_code == 200
    assert isinstance(response.json.get('columns'), list)

def test_search_missing_params(client):
    response = client.get('/api/search')
    assert response.status_code == 400

def test_get_assignment_files(client):
    response = client.get('/assignment-files')
    assert response.status_code == 200
    assert isinstance(response.json, list)
