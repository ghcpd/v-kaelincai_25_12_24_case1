import pytest
import json
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestCouponCalculate:
    def test_zero_discount_rate_causes_error(self, client):
        """When discount_rate is 0, should return 400 error"""
        payload = {'original_price': 100, 'discount_rate': 0}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'discount_rate must be greater than 0' in data['error']

    def test_missing_original_price(self, client):
        """Should return 400 error when original_price is missing"""
        payload = {'discount_rate': 0.8}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'original_price' in data['error']

    def test_missing_discount_rate(self, client):
        """Should return 400 error when discount_rate is missing"""
        payload = {'original_price': 100}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'discount_rate' in data['error']

    def test_negative_discount_rate(self, client):
        """Negative discount rate should be rejected"""
        payload = {'original_price': 100, 'discount_rate': -0.1}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'discount_rate must be greater than 0' in data['error']

    def test_discount_rate_greater_than_one(self, client):
        """Discount rate greater than 1 should be rejected"""
        payload = {'original_price': 100, 'discount_rate': 1.5}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'discount_rate must be greater than 0' in data['error']

    def test_invalid_json(self, client):
        """Invalid JSON should return 400"""
        response = client.post('/api/coupons/calculate',
                              data='invalid json',
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_non_numeric_original_price(self, client):
        """Non-numeric original_price should return 400"""
        payload = {'original_price': 'abc', 'discount_rate': 0.8}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'numeric' in data['error']

    def test_non_numeric_discount_rate(self, client):
        """Non-numeric discount_rate should return 400"""
        payload = {'original_price': 100, 'discount_rate': 'abc'}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'numeric' in data['error']

    def test_valid_calculation(self, client):
        """Valid calculation should return correct result"""
        payload = {'original_price': 100, 'discount_rate': 0.8}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['original_price'] == 100
        assert data['discount_rate'] == 0.8
        assert data['final_price'] == 80.0
        assert data['saved_amount'] == 20.0

    def test_boundary_discount_rate_one(self, client):
        """Discount rate of 1 should be valid (no discount)"""
        payload = {'original_price': 100, 'discount_rate': 1.0}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['final_price'] == 100.0
        assert data['saved_amount'] == 0.0

    def test_float_values(self, client):
        """Float values should work"""
        payload = {'original_price': 99.99, 'discount_rate': 0.5}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['final_price'] == 49.995  # 99.99 * 0.5
        assert data['saved_amount'] == 49.995