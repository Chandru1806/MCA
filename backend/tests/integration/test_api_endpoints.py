import pytest
import json

class TestAuthAPI:
    
    def test_signup_endpoint(self, client):
        unique_id = id(client)
        response = client.post('/api/auth/signup', json={
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'username': f'user_{unique_id}',
            'email': f'user_{unique_id}@test.com',
            'password': 'testpass'
        })
        assert response.status_code in [200, 201]
    
    def test_login_endpoint(self, client):
        unique_id = id(client)
        username = f'loginuser_{unique_id}'
        # First signup
        client.post('/api/auth/signup', json={
            'first_name': 'FirstName',
            'last_name': 'LastName',
            'username': username,
            'email': f'{username}@test.com',
            'password': 'testpass'
        })
        
        # Then login
        response = client.post('/api/auth/login', json={
            'username': username,
            'password': 'testpass'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data

class TestTransactionAPI:
    
    def test_get_transactions(self, client, sample_transaction):
        response = client.get(f'/api/transactions/statement/{sample_transaction.statement_id}')
        assert response.status_code in [200, 401]
    
    def test_import_transactions(self, client):
        response = client.post('/api/transactions/import')
        assert response.status_code in [400, 401]

class TestCategorizationAPI:
    
    def test_categorize_endpoint(self, client, sample_statement):
        response = client.post(f'/api/categorization/categorize/{sample_statement.statement_id}')
        assert response.status_code in [200, 401]

class TestDashboardAPI:
    
    def test_category_summary(self, client, sample_user):
        response = client.get('/api/dashboard/category-summary')
        assert response.status_code in [200, 401]
    
    def test_spending_trends(self, client):
        response = client.get('/api/dashboard/spending-trends')
        assert response.status_code in [200, 401]

class TestAnalyticsAPI:
    
    def test_forecast_endpoint(self, client):
        response = client.post('/api/analytics/forecast', json={
            'target_month': '2024-02',
            'categories': ['Shopping']
        })
        assert response.status_code in [200, 401]
    
    def test_savings_potential(self, client):
        response = client.post('/api/analytics/savings', json={
            'category': 'Shopping',
            'budget_limit': 5000
        })
        assert response.status_code in [200, 401]
