# Project Repair Task Prompt

## Task Objective

Please analyze the following problematic Python Flask project and create a complete fixed version in a new directory. **Do not modify the original project**, but create a brand new directory `fixed_project/`.

---

## Original Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   └── app.py              # Flask application main file (contains bug)
├── tests/
│   ├── __init__.py
│   └── test_coupon.py      # Test file (contains failing tests)
├── data/
│   └── test_cases.json     # Test case data
├── requirements.txt        # Project dependencies
├── README.md               # Project description
└── KNOWN_ISSUE.md          # Known issues detailed documentation
```

---

## Original Project Core Code

### src/app.py (Buggy Version)
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/coupons/calculate', methods=['POST'])
def calculate():
    data = request.json
    
    # Get parameters directly without any validation
    original_price = data.get('original_price')
    discount_rate = data.get('discount_rate')
    
    # ⚠️ Bug: Direct division operation without checking if divisor is zero
    # When discount_rate is 0, it will trigger ZeroDivisionError
    final_price = original_price / discount_rate
    
    saved_amount = original_price - final_price
    
    return jsonify({
        'original_price': original_price,
        'discount_rate': discount_rate,
        'final_price': final_price,
        'saved_amount': saved_amount
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### tests/test_coupon.py (Currently Failing Tests)
```python
import pytest
import json
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestCouponCalculate:
    def test_zero_discount_rate_causes_error(self, client):
        """When discount_rate is 0, should return 400 error, but actually returns 500"""
        payload = {'original_price': 100, 'discount_rate': 0}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400  # Expects 400, actually gets 500
        
    def test_missing_parameters(self, client):
        """Should return 400 error when required parameters are missing"""
        payload = {'original_price': 100}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
        
    def test_negative_discount_rate(self, client):
        """Negative discount rate should be rejected"""
        payload = {'original_price': 100, 'discount_rate': -0.1}
        response = client.post('/api/coupons/calculate',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
```

---

## Known Issues List

### Issue #1: Division-by-Zero Error (ZeroDivisionError)
- **Location**: `src/app.py` line 32
- **Cause**: When `discount_rate` is 0, executing `original_price / discount_rate` causes crash
- **Current Behavior**: Returns HTTP 500 error
- **Expected Behavior**: Returns HTTP 400 error with friendly error message

### Issue #2: Missing Input Parameter Validation
- **Problem**: Does not validate whether required parameters exist
- **Impact**: Throws `TypeError` or `AttributeError` when parameters are missing
- **Expected**: Should check if `original_price` and `discount_rate` exist

### Issue #3: Missing Parameter Range Validation
- **Problem**: Does not check if `discount_rate` is within valid range (0-1)
- **Impact**: Negative values or values greater than 1 lead to unreasonable calculation results
- **Expected**: Should reject values outside valid range

### Issue #4: Business Logic Error
- **Problem**: Uses division `original_price / discount_rate` instead of multiplication
- **Impact**: Calculation results are completely wrong (e.g., 100 / 0.8 = 125, should be 100 * 0.8 = 80)
- **Expected**: Should use correct discount calculation formula

### Issue #5: Missing Error Handling Mechanism
- **Problem**: No try-except blocks to catch exceptions
- **Impact**: Any unexpected errors cause 500 errors
- **Expected**: Should have unified error handling mechanism

---

## Repair Requirements

### 1. Create New Project Directory Structure

Please create a complete fixed version in the `fixed_project/` directory with the following structure:

```
fixed_project/
├── src/
│   ├── __init__.py
│   └── app.py                    # Fixed Flask application (Required)
├── tests/
│   ├── __init__.py
│   └── test_coupon.py            # Updated test file (Required)
├── data/
│   └── test_cases.json           # Test case data (Optional, can copy original)
├── requirements.txt              # Project dependencies (Required)
├── README.md                     # Updated project description (Required)
├── CHANGELOG.md                  # Fix changelog (Required, record all fixes)
└── .gitignore                    # Git ignore file (Optional, recommended)
```

### 2. Core Fix Points

#### src/app.py must include:
- ✅ Input parameter existence validation
- ✅ Division-by-zero check (discount_rate != 0)
- ✅ Parameter range validation (0 < discount_rate <= 1)
- ✅ Parameter type validation (must be numeric)
- ✅ Correct business logic (use multiplication instead of division)
- ✅ Unified error handling mechanism (try-except)
- ✅ Return clear JSON error messages

#### tests/test_coupon.py must include:
- ✅ All original test cases (modified to adapt to fixed code)
- ✅ Additional boundary test cases
- ✅ Ensure all tests pass

#### CHANGELOG.md must include:
- ✅ List of fixed issues
- ✅ Specific code change descriptions
- ✅ Before and after behavior comparison

#### README.md must include:
- ✅ Project overview (this is the fixed version)
- ✅ Installation and running instructions
- ✅ API documentation
- ✅ Test running instructions

---

## Acceptance Criteria

The fixed project must meet the following conditions:

1. **All tests pass**: Running `pytest tests/test_coupon.py -v` all tests must pass (0 failed)
2. **Correct error handling**: 
   - `discount_rate = 0` → Returns HTTP 400, clear error message
   - Missing parameters → Returns HTTP 400, indicates which parameter is missing
   - Negative or out of range → Returns HTTP 400, indicates valid range
3. **Correct business logic**: `original_price = 100, discount_rate = 0.8` → `final_price = 80`
4. **Code quality**: 
   - Appropriate comments
   - Follows Python coding standards (PEP 8)
   - Functions have docstrings
5. **Complete documentation**: CHANGELOG.md clearly records all fixes

---

## Test Verification Steps

After fixing, please verify with the following steps:

1. Install dependencies:
   ```powershell
   cd fixed_project
   pip install -r requirements.txt
   ```

2. Run tests:
   ```powershell
   pytest tests/test_coupon.py -v
   ```

3. Manual testing (optional):
   ```powershell
   # Start service
   python src/app.py
   
   # Test normal request
   curl -X POST http://localhost:5000/api/coupons/calculate ^
     -H "Content-Type: application/json" ^
     -d "{\"original_price\": 100, \"discount_rate\": 0.8}"
   
   # Test division-by-zero case (should return 400 error)
   curl -X POST http://localhost:5000/api/coupons/calculate ^
     -H "Content-Type: application/json" ^
     -d "{\"original_price\": 100, \"discount_rate\": 0}"
   ```

---

## Important Reminders

1. **Do not modify any files in the `issue_project/` directory**
2. **All fixed code must be created in the new `fixed_project/` directory**
3. **Ensure CHANGELOG.md records every fix in detail**
4. **Ensure all tests pass before submission**

---

## Expected Output

Upon completion, you should have:
1. Created a complete `fixed_project/` directory with all required files
2. All tests passing (0 failed)
3. Provide a brief repair summary explaining what issues were fixed
