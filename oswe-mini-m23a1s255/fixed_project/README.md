# Fixed Coupon Service

This repository contains a fixed version of the Coupon Service (Flask) with
proper validation, business-logic correction, and comprehensive tests.

## Summary
- Fixed division-by-zero and incorrect calculation (used multiplication).
- Added input validation, type checks and unified error handling.
- Extended tests and added boundary cases.

## API
POST /api/coupons/calculate
- Request JSON: { "original_price": number, "discount_rate": number }
- Rules: 0 < discount_rate <= 1, original_price >= 0
- Response (200): { original_price, discount_rate, final_price, saved_amount }
- Error (400): { "error": "..." }

## Quick start
1. Create & activate virtualenv (recommended)
2. Install:
   pip install -r requirements.txt
3. Run tests:
   pytest tests/test_coupon.py -q
4. Run the app locally:
   python src/app.py

## Examples
- Normal: {"original_price":100, "discount_rate":0.8} -> final_price: 80.0
- Error: {"original_price":100, "discount_rate":0} -> 400 Bad Request

## License
MIT
