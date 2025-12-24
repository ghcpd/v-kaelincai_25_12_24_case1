# Known Issues Documentation (KNOWN_ISSUE.md)

## Issue #1: Division-by-Zero Error Due to Missing Input Validation

### Issue Classification
- **Type**: Missing Input Validation
- **Severity**: High
- **Impact**: Service crash, returns HTTP 500 error

---

## Issue Details

### 1. Issue Description

The coupon calculation endpoint `POST /api/coupons/calculate` performs division operations directly on input parameters without checking if the divisor is zero. When a client passes `discount_rate: 0`, it triggers a Python `ZeroDivisionError` exception, causing the request to fail and return an HTTP 500 error.

### 2. Root Cause

**File**: `src/app.py`  
**Function**: `calculate()`  
**Problem Code** (Lines 27-32):

```python
data = request.json

# Get parameters directly without any validation
original_price = data.get('original_price')
discount_rate = data.get('discount_rate')

# ⚠️ Problem: Direct division operation without checking if divisor is zero
final_price = original_price / discount_rate  # Line 32
```

**Problem Analysis**:
1. Does not validate if `discount_rate` is `None`
2. Does not check if `discount_rate` is `0`
3. Does not validate the valid range of `discount_rate` (should be between 0-1)
4. Missing `try-except` exception handling mechanism

### 3. Trigger Condition

Any request meeting the following conditions will trigger this issue:

```json
{
  "original_price": 100,
  "discount_rate": 0
}
```

### 4. Expected vs. Actual Behavior

| Aspect | Expected Behavior | Actual Behavior |
|--------|-------------------|------------------|
| **HTTP Status Code** | 400 Bad Request | 500 Internal Server Error |
| **Response Content** | JSON-formatted error message | HTML error page or plain text |
| **Error Message** | `{"error": "discount_rate cannot be zero"}` | `ZeroDivisionError: division by zero` |
| **Service Status** | Continues running, single request fails | Single request crashes, exception logged |

### 5. Error Stack Example

```
Traceback (most recent call last):
  File "c:\BugBash\issue_project\src\app.py", line 32, in calculate
    final_price = original_price / discount_rate
ZeroDivisionError: division by zero
```

### 6. Impact Scope

- **User Experience**: Users see "Internal Server Error" without understanding the cause
- **Log Pollution**: Numerous 500 errors create noise in logs, affecting troubleshooting
- **Security**: Development mode exposes detailed debug information (Werkzeug debugger)
- **Availability**: While individual requests fail, high-frequency triggers affect monitoring alerts

---

## Reproduction Steps

### Reproduce with Automated Tests

```powershell
pytest tests/test_coupon.py::TestCouponCalculate::test_zero_discount_rate_causes_error -v
```

**Expected Result**: Test fails, assertion `status_code == 400` fails, actual result is `500`

### Manual Reproduction with curl

```bash
curl -X POST http://localhost:5000/api/coupons/calculate \
  -H "Content-Type: application/json" \
  -d '{"original_price": 100, "discount_rate": 0}'
```

**Actual Response**:
```
HTTP/1.1 500 INTERNAL SERVER ERROR
Content-Type: text/html; charset=utf-8

<!doctype html>
<html lang=en>
  <title>500 Internal Server Error</title>
  ...
  ZeroDivisionError: division by zero
  ...
```

---

## Fix Approaches

### Approach 1: Add Parameter Validation (Recommended)

Add input validation at the beginning of the `calculate()` function:

```python
@app.route('/api/coupons/calculate', methods=['POST'])
def calculate():
    data = request.json
    
    # Parameter validation
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    original_price = data.get('original_price')
    discount_rate = data.get('discount_rate')
    
    # Check required parameters
    if original_price is None or discount_rate is None:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Type and range validation
    try:
        original_price = float(original_price)
        discount_rate = float(discount_rate)
    except (TypeError, ValueError):
        return jsonify({'error': 'Parameters must be numeric'}), 400
    
    # Business logic validation
    if discount_rate == 0:
        return jsonify({'error': 'discount_rate cannot be zero'}), 400
    
    if discount_rate < 0 or discount_rate > 1:
        return jsonify({'error': 'discount_rate must be between 0 and 1'}), 400
    
    if original_price < 0:
        return jsonify({'error': 'original_price must be positive'}), 400
    
    # Continue with normal logic...
    final_price = original_price / discount_rate
    # ...
```

### Approach 2: Use Exception Handling

```python
try:
    final_price = original_price / discount_rate
except ZeroDivisionError:
    return jsonify({'error': 'discount_rate cannot be zero'}), 400
except TypeError:
    return jsonify({'error': 'Invalid parameter types'}), 400
```

### Approach 3: Use Third-Party Libraries (e.g., Flask-RESTful or marshmallow)

Use schema validation frameworks to automatically handle parameter validation.

---

## Additional Issue Found

### Issue #2: Incorrect Business Logic

Even after fixing the division-by-zero error, the current calculation logic is incorrect:

```python
final_price = original_price / discount_rate  # ❌ Wrong
```

**Correct logic should be**:
```python
final_price = original_price * discount_rate  # ✅ Correct
# Or
final_price = original_price * (1 - discount_rate)  # If discount_rate represents discount percentage
```

**Example**:
- Original price 100, 80% off (discount_rate = 0.8)
- Current calculation: 100 / 0.8 = 125 ❌
- Correct calculation: 100 * 0.8 = 80 ✅

---

## Recommendations to Prevent Similar Issues

1. **Input Validation Layer**: Add unified parameter validation decorators for all API endpoints
2. **Unit Test Coverage**: Ensure boundary conditions (0, negative, None, empty strings, etc.) are tested
3. **Schema Validation**: Use Pydantic or marshmallow to define request models
4. **Error Handlers**: Register global exception handlers for unified response format
5. **API Documentation**: Use Swagger/OpenAPI to explicitly define parameter constraints
6. **Code Review**: Pay special attention to mathematical operations and division during reviews
7. **Static Analysis**: Use tools like pylint, mypy to detect potential issues

---

## References

- [Flask Error Handling](https://flask.palletsprojects.com/en/3.0.x/errorhandling/)
- [Python Exception Handling Best Practices](https://docs.python.org/3/tutorial/errors.html)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-16  
**Status**: Unfixed (deliberately kept for demonstration)
