import json

def test_login_success(client):
    # Create user first
    client.post('/api/auth/profiles',
        data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'SecurePass123'
        }),
        content_type='application/json'
    )
    
    # Login
    response = client.post('/api/auth/login',
        data=json.dumps({
            'username': 'johndoe',
            'password': 'SecurePass123'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['message'] == 'Login successful'
    assert 'access_token' in data['data']
    assert 'refresh_token' in data['data']
    assert data['data']['user']['username'] == 'johndoe'

def test_login_invalid_username(client):
    response = client.post('/api/auth/login',
        data=json.dumps({
            'username': 'nonexistent',
            'password': 'SecurePass123'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] == False
    assert data['error']['code'] == 'INVALID_CREDENTIALS'

def test_login_invalid_password(client):
    # Create user first
    client.post('/api/auth/profiles',
        data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'SecurePass123'
        }),
        content_type='application/json'
    )
    
    # Login with wrong password
    response = client.post('/api/auth/login',
        data=json.dumps({
            'username': 'johndoe',
            'password': 'WrongPassword'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] == False
    assert data['error']['code'] == 'INVALID_CREDENTIALS'

def test_login_missing_fields(client):
    response = client.post('/api/auth/login',
        data=json.dumps({
            'username': 'johndoe'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] == False
    assert data['error']['code'] == 'INVALID_INPUT'
