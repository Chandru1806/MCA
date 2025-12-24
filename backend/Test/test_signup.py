import json

def test_signup_success(client):
    response = client.post('/api/auth/profiles', 
        data=json.dumps({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'SecurePass123'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['message'] == 'Profile created successfully'
    assert 'access_token' in data['data']
    assert 'refresh_token' in data['data']
    assert data['data']['user']['username'] == 'johndoe'

def test_signup_duplicate_username(client):
    # Create first user
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
    
    # Try duplicate username
    response = client.post('/api/auth/profiles',
        data=json.dumps({
            'first_name': 'Jane',
            'last_name': 'Smith',
            'username': 'johndoe',
            'email': 'jane@example.com',
            'password': 'SecurePass456'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert data['success'] == False
    assert data['error']['code'] == 'DUPLICATE_USERNAME'

def test_signup_duplicate_email(client):
    # Create first user
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
    
    # Try duplicate email
    response = client.post('/api/auth/profiles',
        data=json.dumps({
            'first_name': 'Jane',
            'last_name': 'Smith',
            'username': 'janesmith',
            'email': 'john@example.com',
            'password': 'SecurePass456'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert data['success'] == False
    assert data['error']['code'] == 'DUPLICATE_EMAIL'

def test_signup_invalid_input(client):
    response = client.post('/api/auth/profiles',
        data=json.dumps({
            'first_name': 'John',
            'username': 'jo',
            'email': 'invalid-email',
            'password': '123'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] == False
    assert data['error']['code'] == 'INVALID_INPUT'
