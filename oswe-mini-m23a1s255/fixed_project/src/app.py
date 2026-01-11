"""Fixed Coupon Service - Flask application

This module provides a robust, validated implementation of the coupon
calculation endpoint with proper error handling and input validation.
"""
from typing import Any, Dict
from flask import Flask, request, jsonify

app = Flask(__name__)


class BadRequestError(ValueError):
    """Custom error used for 400 responses."""


def _error_response(message: str, status_code: int = 400) -> Any:
    """Return a JSON error response with given status code."""
    return jsonify({"error": message}), status_code


@app.errorhandler(BadRequestError)
def handle_bad_request(err):
    return _error_response(str(err), 400)


@app.errorhandler(400)
def handle_400(err):
    return _error_response("bad request" if not getattr(err, "description", None) else err.description, 400)


@app.errorhandler(Exception)
def handle_generic_error(err):
    # Log the error in real applications (omitted here for brevity)
    return jsonify({"error": "internal server error"}), 500


@app.route("/api/coupons/calculate", methods=["POST"])
def calculate():
    """Calculate discounted price with validation.

    Expected JSON body:
      {
        "original_price": <number>,
        "discount_rate": <number>  # 0 < discount_rate <= 1
      }

    Returns JSON with original_price, discount_rate, final_price and saved_amount.
    """
    data: Dict[str, Any] = request.get_json(silent=True)
    if not data:
        raise BadRequestError("request body must be valid JSON")

    # Required parameters
    if "original_price" not in data:
        raise BadRequestError("missing required parameter: original_price")
    if "discount_rate" not in data:
        raise BadRequestError("missing required parameter: discount_rate")

    # Type coercion & validation
    try:
        original_price = float(data["original_price"])
    except (TypeError, ValueError):
        raise BadRequestError("original_price must be a number")

    try:
        discount_rate = float(data["discount_rate"])
    except (TypeError, ValueError):
        raise BadRequestError("discount_rate must be a number between 0 and 1")

    # Range checks
    if discount_rate == 0:
        raise BadRequestError("discount_rate cannot be zero; must be > 0 and <= 1")
    if not (0 < discount_rate <= 1):
        raise BadRequestError("discount_rate must be > 0 and <= 1")
    if original_price < 0:
        raise BadRequestError("original_price must be >= 0")

    # Business logic: multiply (not divide)
    final_price = round(original_price * discount_rate, 2)
    saved_amount = round(original_price - final_price, 2)

    return jsonify({
        "original_price": original_price,
        "discount_rate": discount_rate,
        "final_price": final_price,
        "saved_amount": saved_amount,
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
