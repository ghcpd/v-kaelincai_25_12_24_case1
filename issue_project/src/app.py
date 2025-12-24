"""
Coupon Service - Flask Application

Provides coupon discount calculation functionality
"""
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/coupons/calculate', methods=['POST'])
def calculate():
    """
    Calculate discounted price
    
    Request body:
        {
            "original_price": float,  # Original price
            "discount_rate": float    # Discount rate (between 0-1)
        }
    
    Response:
        {
            "original_price": float,
            "discount_rate": float,
            "final_price": float,
            "saved_amount": float
        }
    """
    data = request.json
    
    # Get parameters directly without any validation
    original_price = data.get('original_price')
    discount_rate = data.get('discount_rate')
    
    # ⚠️ Bug: Direct division operation without checking if divisor is zero
    # When discount_rate is 0, it will trigger ZeroDivisionError
    final_price = original_price / discount_rate
    
    saved_amount = original_price - final_price
    
    return jsonify({
        'original_price': original_price,
        'discount_rate': discount_rate,
        'final_price': final_price,
        'saved_amount': saved_amount
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
