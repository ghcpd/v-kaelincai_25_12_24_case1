# CHANGELOG

All notable changes to the fixed project are documented here.

## [Unreleased]
- Fixed Issue #1: Division-by-zero
  - Before: `final_price` computed with division -> raised ZeroDivisionError for discount_rate = 0 -> HTTP 500
  - After: Request validated; discount_rate == 0 returns HTTP 400 with a helpful message
- Fixed Issue #2: Missing Input Parameter Validation
  - Before: Missing parameters raised TypeError/AttributeError -> HTTP 500
  - After: Presence and type checks added; missing parameters return HTTP 400 and indicate which parameter is missing
- Fixed Issue #3: Parameter Range Validation
  - Before: Negative or >1 discount_rate accepted and produced invalid results
  - After: Rejects discount_rate outside (0,1] with HTTP 400
- Fixed Issue #4: Business Logic Error
  - Before: Used division (original_price / discount_rate)
  - After: Uses correct calculation final_price = original_price * discount_rate
- Fixed Issue #5: Missing Error Handling Mechanism
  - Before: Unhandled exceptions produced HTTP 500
  - After: Try/except and clear JSON errors, with unified fallback for unexpected exceptions

Notes: See `src/app.py` and `tests/test_coupon.py` for implementation details and test coverage.
