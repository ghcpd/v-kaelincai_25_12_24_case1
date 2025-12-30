# Changelog

All changes made to fix the issues in the original project.

## Fixed Issues

### Issue #1: Division-by-Zero Error
- **Before**: `final_price = original_price / discount_rate` caused ZeroDivisionError when discount_rate = 0
- **After**: Changed to `final_price = original_price * discount_rate` and added validation to reject discount_rate <= 0
- **Impact**: Now returns HTTP 400 with error message instead of 500 crash

### Issue #2: Missing Input Parameter Validation
- **Before**: No checks for missing parameters, caused TypeError
- **After**: Added checks for presence of `original_price` and `discount_rate`
- **Impact**: Returns HTTP 400 with specific missing parameter message

### Issue #3: Missing Parameter Range Validation
- **Before**: No validation for discount_rate range
- **After**: Added validation: 0 < discount_rate <= 1
- **Impact**: Rejects invalid ranges with HTTP 400

### Issue #4: Business Logic Error
- **Before**: Used division instead of multiplication for discount calculation
- **After**: Corrected to `final_price = original_price * discount_rate`
- **Impact**: Correct calculation results (e.g., 100 * 0.8 = 80 instead of 100 / 0.8 = 125)

### Issue #5: Missing Error Handling Mechanism
- **Before**: No try-except, unexpected errors caused 500
- **After**: Added try-except block with proper error responses
- **Impact**: Graceful error handling

### Additional Improvements
- Added type validation for numeric parameters
- Added rounding to 2 decimal places for prices
- Enhanced test coverage with additional boundary cases
- Improved code documentation with docstrings
- Added proper JSON validation