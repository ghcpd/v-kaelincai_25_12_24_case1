# Coupon Service - Fixed Version

## Project Overview

This is a **fixed version** of the Coupon Service Flask application. All known bugs have been resolved with comprehensive input validation, error handling, and corrected business logic.

## Fixed Issues

### Issue #1: Division-by-Zero Error ✅ FIXED
- **Problem**: When `discount_rate` is 0, the application crashed with ZeroDivisionError (HTTP 500)
- **Solution**: Added zero-check validation that returns HTTP 400 with clear error message
- **Location**: `src/app.py` in `validate_input()` function

### Issue #2: Missing Input Parameter Validation ✅ FIXED
- **Problem**: No validation for missing required parameters
- **Solution**: Added existence checks for both `original_price` and `discount_rate`
- **Location**: `src/app.py` in `validate_input()` function

### Issue #3: Missing Parameter Range Validation ✅ FIXED
- **Problem**: `discount_rate` could be negative or greater than 1
- **Solution**: Added range validation to ensure 0 < discount_rate ≤ 1
- **Location**: `src/app.py` in `validate_input()` function

### Issue #4: Incorrect Business Logic ✅ FIXED
- **Problem**: Used division instead of multiplication (original_price / discount_rate)
- **Solution**: Changed to correct formula (original_price * discount_rate)
- **Location**: `src/app.py` line with `final_price = original_price * discount_rate`
- **Example**: 100 * 0.8 = 80 (correct) instead of 100 / 0.8 = 125 (wrong)

### Issue #5: Missing Type Validation ✅ FIXED
- **Problem**: Non-numeric values would cause TypeErrors
- **Solution**: Added type validation with conversion and error handling
- **Location**: `src/app.py` in `validate_input()` function

### Issue #6: Missing Error Handling Mechanism ✅ FIXED
- **Problem**: Unhandled exceptions would cause 500 errors
- **Solution**: Added try-except blocks and proper error responses
- **Location**: `src/app.py` in `calculate()` function

## Project Structure

```
fixed_project/
├── src/
│   ├── __init__.py               # Package initialization
│   └── app.py                    # Fixed Flask application
├── tests/
│   ├── __init__.py               # Test package initialization
│   └── test_coupon.py            # Comprehensive test suite
├── data/
│   └── test_cases.json           # Test case reference data
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── CHANGELOG.md                  # Detailed change log
└── .gitignore                    # Git ignore file
```

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup Steps

1. Clone or navigate to the project directory:
   ```powershell
   cd fixed_project
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Running the Application

### Development Mode

Start the Flask development server:

```powershell
python src/app.py
```

The server will start on `http://localhost:5000`

### Testing

Run the comprehensive test suite:

```powershell
pytest tests/test_coupon.py -v
```

To run with detailed output:

```powershell
pytest tests/test_coupon.py -vv
```

To run a specific test:

```powershell
pytest tests/test_coupon.py::TestCouponCalculate::test_normal_discount_calculation -v
```

## API Documentation

### Endpoints

#### 1. Health Check
- **Endpoint**: `GET /health`
- **Description**: Check if the service is running
- **Response**: `{"status": "ok"}`

#### 2. Calculate Discount
- **Endpoint**: `POST /api/coupons/calculate`
- **Description**: Calculate the final price after applying a discount rate
- **Content-Type**: `application/json`

### Request Format

```json
{
  "original_price": 100.00,
  "discount_rate": 0.8
}
```

**Parameters:**
- `original_price` (float, required): The original price before discount. Must be > 0.
- `discount_rate` (float, required): The discount rate as a decimal. Must be in range (0, 1] (exclusive of 0, inclusive of 1).

### Response Format (Success - HTTP 200)

```json
{
  "original_price": 100.00,
  "discount_rate": 0.8,
  "final_price": 80.00,
  "saved_amount": 20.00
}
```

**Response Fields:**
- `original_price`: The original price (echoed from request)
- `discount_rate`: The discount rate (echoed from request)
- `final_price`: The calculated final price after discount (original_price * discount_rate)
- `saved_amount`: The amount saved (original_price - final_price)

### Response Format (Error - HTTP 400)

```json
{
  "error": "discount_rate cannot be zero"
}
```

### Error Scenarios

| Scenario | HTTP Status | Error Message |
|----------|------------|---------------|
| `discount_rate = 0` | 400 | `discount_rate cannot be zero` |
| Missing `original_price` | 400 | `Missing required parameter: original_price` |
| Missing `discount_rate` | 400 | `Missing required parameter: discount_rate` |
| `discount_rate < 0` | 400 | `discount_rate must be between 0 and 1...` |
| `discount_rate > 1` | 400 | `discount_rate must be between 0 and 1...` |
| `original_price <= 0` | 400 | `original_price must be greater than 0` |
| Non-numeric `original_price` | 400 | `original_price must be a valid number` |
| Non-numeric `discount_rate` | 400 | `discount_rate must be a valid number` |

## Usage Examples

### Example 1: Normal Discount Calculation

**Request:**
```powershell
curl -X POST http://localhost:5000/api/coupons/calculate `
  -H "Content-Type: application/json" `
  -d '{"original_price": 100, "discount_rate": 0.8}'
```

**Response:**
```json
{
  "original_price": 100,
  "discount_rate": 0.8,
  "final_price": 80,
  "saved_amount": 20
}
```

### Example 2: Zero Discount Rate (Error)

**Request:**
```powershell
curl -X POST http://localhost:5000/api/coupons/calculate `
  -H "Content-Type: application/json" `
  -d '{"original_price": 100, "discount_rate": 0}'
```

**Response:**
```json
{
  "error": "discount_rate cannot be zero"
}
```

### Example 3: Missing Parameter (Error)

**Request:**
```powershell
curl -X POST http://localhost:5000/api/coupons/calculate `
  -H "Content-Type: application/json" `
  -d '{"original_price": 100}'
```

**Response:**
```json
{
  "error": "Missing required parameter: discount_rate"
}
```

### Example 4: Out of Range Discount Rate (Error)

**Request:**
```powershell
curl -X POST http://localhost:5000/api/coupons/calculate `
  -H "Content-Type: application/json" `
  -d '{"original_price": 100, "discount_rate": 1.5}'
```

**Response:**
```json
{
  "error": "discount_rate must be between 0 and 1 (exclusive of 0, inclusive of 1)"
}
```

## Test Coverage

The test suite includes:

- **Basic Functionality Tests** (3 tests)
  - Health check endpoint
  - Normal discount calculation
  - Decimal price handling

- **Division-by-Zero Tests** (2 tests)
  - Zero discount rate returns 400
  - Error message validation

- **Missing Parameter Tests** (4 tests)
  - Missing discount_rate
  - Missing original_price
  - Missing both parameters
  - Empty request body

- **Parameter Range Tests** (5 tests)
  - Negative discount_rate
  - Discount rate > 1
  - Discount rate = 1 (edge case)
  - Negative original_price
  - Zero original_price

- **Type Validation Tests** (2 tests)
  - Invalid original_price type
  - Invalid discount_rate type

- **Edge Cases** (2 tests)
  - Very small discount rate
  - Very large price value

**Total: 18 comprehensive test cases**

## Version History

- **v2.0 (Current)**: Fixed version with all issues resolved
- **v1.0**: Original buggy version (in issue_project/)

## Dependencies

- **Flask 3.0.0**: Web framework for building the API
- **pytest 7.4.3**: Testing framework

## Code Quality

- ✅ Follows PEP 8 Python coding standards
- ✅ Comprehensive docstrings for all functions
- ✅ Clear error messages
- ✅ Proper type handling and validation
- ✅ Full test coverage of all code paths
- ✅ Comments explaining key logic

## Support

For issues or questions, refer to:
- `CHANGELOG.md` - Detailed list of all fixes
- `src/app.py` - Well-documented source code
- `tests/test_coupon.py` - Test examples showing proper usage

---

**Status**: ✅ All issues fixed and tested. Ready for production.
