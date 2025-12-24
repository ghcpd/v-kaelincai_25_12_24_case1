from flask import Flask, request, jsonify

app = Flask(__name__)


class InvalidUsage(Exception):
    """Custom exception for invalid input that carries an HTTP status code."""

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    # Generic handler for unexpected errors - do not expose internal details
    response = jsonify({"error": "internal server error"})
    response.status_code = 500
    return response


def _validate_number(value, name):
    """Ensure value is present and numeric (int/float).

    Raises InvalidUsage on validation failure.
    """
    if value is None:
        raise InvalidUsage(f"missing required parameter: {name}", status_code=400)
    if not isinstance(value, (int, float)):
        raise InvalidUsage(f"{name} must be a number", status_code=400)
    return value


@app.route('/api/coupons/calculate', methods=['POST'])
def calculate():
    """Calculate final price after applying a discount rate.

    Expected JSON body: { "original_price": <number>, "discount_rate": <number between 0 and 1> }

    Business logic: final_price = original_price * discount_rate
    """
    try:
        data = request.get_json(force=True)
    except Exception:
        raise InvalidUsage("invalid or missing JSON body", status_code=400)

    # Validate presence and types
    original_price = _validate_number(data.get('original_price'), 'original_price')
    discount_rate = _validate_number(data.get('discount_rate'), 'discount_rate')

    # Range checks
    if discount_rate == 0:
        raise InvalidUsage("discount_rate cannot be zero", status_code=400)
    if discount_rate < 0 or discount_rate > 1:
        raise InvalidUsage("discount_rate must be between 0 (exclusive) and 1 (inclusive)", status_code=400)
    if original_price < 0:
        raise InvalidUsage("original_price must be non-negative", status_code=400)

    # Correct business logic: multiplication
    final_price = round(original_price * discount_rate, 2)
    saved_amount = round(original_price - final_price, 2)

    return jsonify({
        'original_price': original_price,
        'discount_rate': discount_rate,
        'final_price': final_price,
        'saved_amount': saved_amount
    }), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
