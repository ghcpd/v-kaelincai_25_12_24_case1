"""
Coupon Service Tests

Contains deliberately failing test cases to reproduce division-by-zero error
"""
import pytest
import json
from src.app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestCouponCalculate:
    """Coupon calculation endpoint tests"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
    
    def test_normal_discount_calculation(self, client):
        """Test normal discount calculation (this test will pass)"""
        payload = {
            'original_price': 100,
            'discount_rate': 0.8  # 80% discount
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Note: Current logic is 100 / 0.8 = 125, which is flawed
        # Correct should be 100 * 0.8 = 80
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['original_price'] == 100
        assert data['discount_rate'] == 0.8
    
    def test_zero_discount_rate_causes_error(self, client):
        """
        ⚠️ This test will fail - Reproduces division-by-zero error
        
        Issue: When discount_rate is 0, should return error response but actually triggers ZeroDivisionError
        Expected: Returns 400 Bad Request with error message
        Actual: Returns 500 Internal Server Error
        """
        payload = {
            'original_price': 100,
            'discount_rate': 0  # Divisor is zero
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Should return 400 error, but actually returns 500
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'discount_rate' in data['error'].lower()
    
    def test_zero_discount_rate_error_message(self, client):
        """
        ⚠️ This test will fail - Validates error message
        
        Issue: Should return friendly error message instead of server crash
        """
        payload = {
            'original_price': 200,
            'discount_rate': 0
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Should have clear error message
        data = json.loads(response.data)
        assert response.status_code == 400
        assert 'error' in data
        assert 'cannot be zero' in data['error'] or 'invalid' in data['error'].lower()
    
    def test_missing_parameters(self, client):
        """Test missing parameters (this test will also fail)"""
        payload = {
            'original_price': 100
            # Missing discount_rate
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Should return 400 error
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_negative_discount_rate(self, client):
        """Test negative discount rate (edge case)"""
        payload = {
            'original_price': 100,
            'discount_rate': -0.1
        }
        response = client.post(
            '/api/coupons/calculate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Should return 400 error
        assert response.status_code == 400


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
