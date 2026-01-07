import pytest
import json
from src.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestCouponCalculate:
    def post(self, client, payload):
        return client.post('/api/coupons/calculate', data=json.dumps(payload), content_type='application/json')

    def test_zero_discount_rate_causes_error(self, client):
        payload = {'original_price': 100, 'discount_rate': 0}
        response = self.post(client, payload)
        assert response.status_code == 400
        assert 'discount_rate' in response.get_json().get('error', '')

    def test_missing_parameters(self, client):
        payload = {'original_price': 100}
        response = self.post(client, payload)
        assert response.status_code == 400
        assert 'Missing parameter' in response.get_json().get('error', '')

    def test_negative_discount_rate(self, client):
        payload = {'original_price': 100, 'discount_rate': -0.1}
        response = self.post(client, payload)
        assert response.status_code == 400

    def test_normal_calculation(self, client):
        payload = {'original_price': 100, 'discount_rate': 0.8}
        response = self.post(client, payload)
        assert response.status_code == 200
        data = response.get_json()
        assert data['final_price'] == 80
        assert data['saved_amount'] == 20

    def test_discount_rate_one(self, client):
        payload = {'original_price': 50, 'discount_rate': 1}
        response = self.post(client, payload)
        assert response.status_code == 200
        data = response.get_json()
        assert data['final_price'] == 50

    def test_non_numeric_parameters(self, client):
        payload = {'original_price': 'a', 'discount_rate': 'b'}
        response = self.post(client, payload)
        assert response.status_code == 400
