import pytest
import json
from src.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestCouponCalculate:
    def post_json(self, client, payload):
        return client.post('/api/coupons/calculate',
                           data=json.dumps(payload),
                           content_type='application/json')

    def test_correct_calculation(self, client):
        payload = {'original_price': 100, 'discount_rate': 0.8}
        resp = self.post_json(client, payload)
        assert resp.status_code == 200
        body = resp.get_json()
        assert body['final_price'] == 80
        assert body['saved_amount'] == 20

    def test_zero_discount_rate_causes_error(self, client):
        payload = {'original_price': 100, 'discount_rate': 0}
        resp = self.post_json(client, payload)
        assert resp.status_code == 400
        assert 'discount_rate cannot be zero' in resp.get_json().get('error', '')

    def test_missing_parameters(self, client):
        payload = {'original_price': 100}
        resp = self.post_json(client, payload)
        assert resp.status_code == 400
        assert 'missing required parameter' in resp.get_json().get('error', '')

    def test_negative_discount_rate(self, client):
        payload = {'original_price': 100, 'discount_rate': -0.1}
        resp = self.post_json(client, payload)
        assert resp.status_code == 400
        assert 'must be between 0' in resp.get_json().get('error', '')

    def test_discount_rate_greater_than_one(self, client):
        payload = {'original_price': 100, 'discount_rate': 1.5}
        resp = self.post_json(client, payload)
        assert resp.status_code == 400
        assert 'must be between 0' in resp.get_json().get('error', '')

    def test_original_price_negative(self, client):
        payload = {'original_price': -10, 'discount_rate': 0.5}
        resp = self.post_json(client, payload)
        assert resp.status_code == 400
        assert 'original_price must be non-negative' in resp.get_json().get('error', '')

    def test_non_numeric_parameters(self, client):
        payload = {'original_price': '100', 'discount_rate': '0.8'}
        resp = self.post_json(client, payload)
        assert resp.status_code == 400
        assert 'must be a number' in resp.get_json().get('error', '')
