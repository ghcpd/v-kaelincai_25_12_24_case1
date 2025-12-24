"""Flask app for coupon calculation (fixed).

Implements input validation, correct calculation logic, and clear error handling.
"""
from typing import Any
from flask import Flask, request, jsonify

app = Flask(__name__)


def _to_number(value: Any, name: str) -> float:
    """Convert value to float and validate existence and type.

    Raises ValueError with a friendly message if invalid.
    """
    if value is None:
        raise ValueError(f"Missing parameter: {name}")
    if isinstance(value, (int, float)):
        return float(value)
    # Try cast if it's a string that looks like a number
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Parameter '{name}' must be a numeric value")


@app.route('/api/coupons/calculate', methods=['POST'])
def calculate():
    """Calculate final price and saved amount given original_price and discount_rate.

    Accepts JSON body with keys:
      - original_price: numeric > 0
      - discount_rate: numeric in (0, 1]

    Returns JSON with final_price and saved_amount on success, or an error message with
    HTTP 400 when input is invalid.
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON payload'}), 400

    try:
        original_price = _to_number(data.get('original_price'), 'original_price')
        discount_rate = _to_number(data.get('discount_rate'), 'discount_rate')

        if original_price < 0:
            return jsonify({'error': 'original_price must be non-negative'}), 400

        # Business rules: discount_rate must be > 0 and <= 1
        if discount_rate == 0:
            return jsonify({'error': 'discount_rate must not be 0'}), 400
        if not (0 < discount_rate <= 1):
            return jsonify({'error': 'discount_rate must be between 0 (exclusive) and 1 (inclusive)'}), 400

        # Correct calculation: multiply, not divide
        final_price = original_price * discount_rate
        saved_amount = original_price - final_price

        return jsonify({
            'original_price': original_price,
            'discount_rate': discount_rate,
            'final_price': final_price,
            'saved_amount': saved_amount
        }), 200

    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception:
        # Unified fallback for unexpected errors
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/health', methods=['GET'])
def health():
    """Simple health-check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
