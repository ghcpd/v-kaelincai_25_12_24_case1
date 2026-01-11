# Changelog

## 2025-12-24 - Fixed version
### Fixed
- Issue #1 (Division-by-zero): Replaced incorrect division with validated multiplication and return 400 when discount_rate is 0. (src/app.py)
- Issue #2 (Missing parameter validation): Added explicit presence checks and clear error messages for missing parameters. (src/app.py)
- Issue #3 (Parameter range validation): Enforced 0 < discount_rate <= 1 and original_price >= 0. (src/app.py)
- Issue #4 (Business logic): Corrected final_price calculation to use multiplication (final_price = original_price * discount_rate). (src/app.py)
- Issue #5 (Error handling): Introduced unified error handling and JSON error responses; prevented 500s for client errors. (src/app.py)

### Tests
- Added boundary and negative tests; updated expectations to match corrected logic. (tests/test_coupon.py)

### Notes
- The original project was not modified; a fixed copy was created under `fixed_project/`.
