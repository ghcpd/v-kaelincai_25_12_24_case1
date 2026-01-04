"""
Coupon Service - Flask Application (FIXED VERSION)

Provides coupon discount calculation functionality with comprehensive input validation
and error handling.

Fixed Issues:
- Added input parameter validation
- Added division-by-zero check
- Added parameter range validation
- Fixed business logic (multiplication instead of division)
- Added comprehensive error handling
"""
from flask import Flask, request, jsonify

app = Flask(__name__)


def validate_input(data):
    """
    Validate input parameters for coupon calculation.
    
    Args:
        data: Request JSON data
        
    Returns:
        tuple: (is_valid, original_price, discount_rate, error_message)
        
    Raises:
        None - returns error details instead
    """
    # Check if data exists
    if not data:
        return False, None, None, "Request body cannot be empty"
    
    # Check if original_price exists
    if 'original_price' not in data:
        return False, None, None, "Missing required parameter: original_price"
    
    # Check if discount_rate exists
    if 'discount_rate' not in data:
        return False, None, None, "Missing required parameter: discount_rate"
    
    original_price = data.get('original_price')
    discount_rate = data.get('discount_rate')
    
    # Validate that original_price is numeric
    try:
        original_price = float(original_price)
    except (TypeError, ValueError):
        return False, None, None, "original_price must be a valid number"
    
    # Validate that discount_rate is numeric
    try:
        discount_rate = float(discount_rate)
    except (TypeError, ValueError):
        return False, None, None, "discount_rate must be a valid number"
    
    # Validate original_price is positive
    if original_price <= 0:
        return False, None, None, "original_price must be greater than 0"
    
    # Validate discount_rate is not zero (division-by-zero check)
    if discount_rate == 0:
        return False, None, None, "discount_rate cannot be zero"
    
    # Validate discount_rate is in valid range (0, 1]
    if discount_rate <= 0 or discount_rate > 1:
        return False, None, None, "discount_rate must be between 0 and 1 (exclusive of 0, inclusive of 1)"
    
    return True, original_price, discount_rate, None


@app.route('/api/coupons/calculate', methods=['POST'])
def calculate():
    """
    Calculate discounted price based on discount rate.
    
    This endpoint calculates the final price after applying a discount rate.
    The final price is calculated as: final_price = original_price * discount_rate
    
    Request body (JSON):
        {
            "original_price": float,  # Original price (must be > 0)
            "discount_rate": float    # Discount rate (must be in range (0, 1])
        }
    
    Response on success (HTTP 200):
        {
            "original_price": float,
            "discount_rate": float,
            "final_price": float,
            "saved_amount": float
        }
    
    Response on error (HTTP 400):
        {
            "error": string  # Error message describing what went wrong
        }
    
    Example requests:
        POST /api/coupons/calculate
        Content-Type: application/json
        
        {
            "original_price": 100,
            "discount_rate": 0.8
        }
        
        Expected response:
        {
            "original_price": 100,
            "discount_rate": 0.8,
            "final_price": 80,
            "saved_amount": 20
        }
    """
    try:
        # Get JSON data from request
        data = request.json
        
        # Validate input parameters
        is_valid, original_price, discount_rate, error_msg = validate_input(data)
        
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # FIXED: Use multiplication instead of division
        # Original (buggy) logic: final_price = original_price / discount_rate
        # Fixed logic: final_price = original_price * discount_rate
        final_price = original_price * discount_rate
        
        # Calculate saved amount
        saved_amount = original_price - final_price
        
        return jsonify({
            'original_price': original_price,
            'discount_rate': discount_rate,
            'final_price': final_price,
            'saved_amount': saved_amount
        }), 200
        
    except Exception as e:
        # Catch any unexpected errors and return 500 with error message
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    
    Returns:
        JSON: {"status": "ok"}
    """
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
