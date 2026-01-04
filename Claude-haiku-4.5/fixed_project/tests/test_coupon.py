"""
Coupon Service Tests (FIXED VERSION)

Contains comprehensive test cases to verify all bugs have been fixed.
"""
import pytest
import json
from src.app import app


@pytest.fixture
def client():
    """Create test client for testing"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestCouponCalculate:
    """Coupon calculation endpoint tests"""
    
    # ===== Basic Functionality Tests =====
    
    def test_health_check(self, client):
        """Test health check endpoint returns 200 OK"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
    
    def test_normal_discount_calculation(self, client):
        """Test normal discount calculation with valid parameters"""
        payload = {
            'original_price': 100,
            'discount_rate': 0.8  # 80% of original price
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['original_price'] == 100
        assert data['discount_rate'] == 0.8
        # FIXED: Now uses multiplication (correct logic)
        assert data['final_price'] == 80  # 100 * 0.8 = 80
        assert data['saved_amount'] == 20  # 100 - 80 = 20
    
    def test_normal_calculation_with_float_prices(self, client):
        """Test calculation with decimal prices"""
        payload = {
            'original_price': 99.99,
            'discount_rate': 0.5
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert abs(data['final_price'] - 49.995) < 0.001  # 99.99 * 0.5
    
    # ===== Issue #1: Division-by-Zero Error Tests =====
    
    def test_zero_discount_rate_returns_400(self, client):
        """
        FIXED: Test that zero discount_rate returns 400 Bad Request
        (Previously returned 500 ZeroDivisionError)
        """
        payload = {
            'original_price': 100,
            'discount_rate': 0
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'discount_rate' in data['error'].lower()
    
    def test_zero_discount_rate_error_message(self, client):
        """FIXED: Verify error message is clear and friendly"""
        payload = {
            'original_price': 200,
            'discount_rate': 0
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        assert response.status_code == 400
        assert 'error' in data
        assert 'cannot be zero' in data['error'].lower()
    
    # ===== Issue #2: Missing Parameter Validation Tests =====
    
    def test_missing_discount_rate_parameter(self, client):
        """FIXED: Test missing discount_rate parameter returns 400"""
        payload = {
            'original_price': 100
            # Missing discount_rate
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'discount_rate' in data['error'].lower()
    
    def test_missing_original_price_parameter(self, client):
        """FIXED: Test missing original_price parameter returns 400"""
        payload = {
            'discount_rate': 0.8
            # Missing original_price
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'original_price' in data['error'].lower()
    
    def test_missing_both_parameters(self, client):
        """FIXED: Test missing both parameters returns 400"""
        payload = {}
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_empty_request_body(self, client):
        """FIXED: Test empty request body returns 400"""
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(None),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    # ===== Issue #3: Parameter Range Validation Tests =====
    
    def test_negative_discount_rate(self, client):
        """FIXED: Test negative discount rate returns 400"""
        payload = {
            'original_price': 100,
            'discount_rate': -0.1
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_discount_rate_greater_than_one(self, client):
        """FIXED: Test discount_rate > 1 returns 400"""
        payload = {
            'original_price': 100,
            'discount_rate': 1.5
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_discount_rate_exactly_one(self, client):
        """Test discount_rate = 1 (100% of original price) is valid"""
        payload = {
            'original_price': 100,
            'discount_rate': 1.0
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['final_price'] == 100
        assert data['saved_amount'] == 0
    
    def test_negative_original_price(self, client):
        """FIXED: Test negative original_price returns 400"""
        payload = {
            'original_price': -100,
            'discount_rate': 0.8
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_zero_original_price(self, client):
        """FIXED: Test zero original_price returns 400"""
        payload = {
            'original_price': 0,
            'discount_rate': 0.8
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    # ===== Issue #4: Type Validation Tests =====
    
    def test_invalid_original_price_type(self, client):
        """FIXED: Test non-numeric original_price returns 400"""
        payload = {
            'original_price': 'not_a_number',
            'discount_rate': 0.8
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_invalid_discount_rate_type(self, client):
        """FIXED: Test non-numeric discount_rate returns 400"""
        payload = {
            'original_price': 100,
            'discount_rate': 'not_a_number'
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    # ===== Edge Cases =====
    
    def test_very_small_discount_rate(self, client):
        """Test with very small but valid discount rate"""
        payload = {
            'original_price': 100,
            'discount_rate': 0.001
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert abs(data['final_price'] - 0.1) < 0.001  # 100 * 0.001
    
    def test_very_large_price(self, client):
        """Test with very large price value"""
        payload = {
            'original_price': 999999.99,
            'discount_rate': 0.5
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert abs(data['final_price'] - 499999.995) < 0.001


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
