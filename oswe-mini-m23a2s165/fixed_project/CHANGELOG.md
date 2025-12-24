# CHANGELOG

All notable changes made to fix the coupon calculator service.

## [Unreleased]
- Fixed division-by-zero crash (returned 500) → now returns 400 with `discount_rate cannot be zero`.
- Added input presence checks for `original_price` and `discount_rate` (returns 400 with which parameter is missing).
- Added numeric type validation for parameters (returns 400 for non-numeric inputs).
- Enforced parameter ranges: `discount_rate` must be 0 < rate <= 1; `original_price` must be >= 0.
- Corrected business logic: replaced `original_price / discount_rate` with `original_price * discount_rate`.
- Added unified error handling with clear JSON error messages and proper status codes.
- Extended unit tests to include boundary cases and invalid-input tests.

### Before / After
- Before: `final_price` computed with division and caused ZeroDivisionError for `discount_rate=0` (HTTP 500).
- After: `final_price = original_price * discount_rate`; invalid inputs return HTTP 400 and a clear error message.
