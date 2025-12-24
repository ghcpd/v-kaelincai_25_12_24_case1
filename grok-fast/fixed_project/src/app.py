from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

@app.route('/api/coupons/calculate', methods=['POST'])
def calculate():
    """
    Calculate the final price after applying a discount rate.

    Expects JSON payload with:
    - original_price: float or int, the original price
    - discount_rate: float between 0 and 1 (exclusive of 0), the discount multiplier

    Returns:
    - JSON with original_price, discount_rate, final_price, saved_amount
    - Or error JSON with message and status 400
    """
    try:
        data = request.get_json()
    except BadRequest:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    try:
        if not data:
            return jsonify({'error': 'Invalid JSON payload'}), 400

        # Validate required parameters
        original_price = data.get('original_price')
        discount_rate = data.get('discount_rate')

        if original_price is None:
            return jsonify({'error': 'Missing required parameter: original_price'}), 400
        if discount_rate is None:
            return jsonify({'error': 'Missing required parameter: discount_rate'}), 400

        # Validate types
        try:
            original_price = float(original_price)
            discount_rate = float(discount_rate)
        except (ValueError, TypeError):
            return jsonify({'error': 'Parameters must be numeric'}), 400

        # Validate ranges
        if discount_rate <= 0 or discount_rate > 1:
            return jsonify({'error': 'discount_rate must be greater than 0 and less than or equal to 1'}), 400

        # Calculate
        final_price = original_price * discount_rate
        saved_amount = original_price - final_price

        return jsonify({
            'original_price': original_price,
            'discount_rate': discount_rate,
            'final_price': final_price,
            'saved_amount': saved_amount
        })

    except Exception as e:
        # Catch any unexpected errors
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)