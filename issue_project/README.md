# Coupon Service - Bug Reproduction Project

## Project Overview

This is a Flask coupon service project with a deliberately planted division-by-zero error, designed to demonstrate and reproduce service crashes caused by missing input parameter validation.

## Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   └── app.py              # Flask application main file (contains the bug)
├── tests/
│   ├── __init__.py
│   └── test_coupon.py      # Test file (contains failing tests)
├── data/
│   └── test_cases.json     # Test case data
├── requirements.txt        # Project dependencies
├── README.md               # This file
└── KNOWN_ISSUE.md          # Known issues detailed documentation
```

## Issue Overview

**System**: Coupon Service  
**Endpoint**: `POST /api/coupons/calculate`  
**Issue Type**: Missing input parameter validation, leading to division-by-zero error (ZeroDivisionError)

### Trigger Condition

When a client sends a request with `discount_rate` set to `0`, the server triggers a division-by-zero error and returns HTTP 500.

### Expected vs. Actual Behavior

- **Expected**: Returns HTTP 400 Bad Request with a friendly error message
- **Actual**: Returns HTTP 500 Internal Server Error, service crashes with Python traceback output

## Quick Start

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Run Tests (expect failures)

```powershell
pytest tests/test_coupon.py -v
```

**Expected Result**: At least 3 tests fail, demonstrating the issue

### 3. Manual Service Testing (Optional)

Start the service:
```powershell
python src/app.py
```

Send requests using curl or PowerShell:
```powershell
# Normal request
curl -X POST http://localhost:5000/api/coupons/calculate `
  -H "Content-Type: application/json" `
  -d '{\"original_price\": 100, \"discount_rate\": 0.8}'

# Trigger division-by-zero error
curl -X POST http://localhost:5000/api/coupons/calculate `
  -H "Content-Type: application/json" `
  -d '{\"original_price\": 100, \"discount_rate\": 0}'
```

## Test Description

### Passing Tests
- `test_health_check`: Health check endpoint
- `test_normal_discount_calculation`: Normal discount calculation (but logic is flawed)

### Failing Tests (Reproduce the Issue)
- ⚠️ `test_zero_discount_rate_causes_error`: Reproduces division-by-zero error, expects 400 but gets 500
- ⚠️ `test_zero_discount_rate_error_message`: Validates error message, missing friendly feedback
- ⚠️ `test_missing_parameters`: Missing parameters not validated
- ⚠️ `test_negative_discount_rate`: Negative discount rate not rejected

## Tech Stack

- **Python**: 3.8+
- **Flask**: 3.0.0
- **pytest**: 7.4.3
- **Operating System**: Windows 11

## Core Bug Code Location

**File**: `src/app.py`  
**Function**: `calculate()`  
**Line**: Around line 32

```python
# ⚠️ Bug: Direct division operation without checking if divisor is zero
final_price = original_price / discount_rate
```

## Next Steps

1. Run tests to see failure scenarios
2. Read `KNOWN_ISSUE.md` to understand issue details and fix approaches
3. Fix the code as needed and verify tests pass

## Important Note

⚠️ **This is a demonstration project with deliberate bugs. Do NOT use in production!**

## License

MIT License - For learning and testing purposes only
