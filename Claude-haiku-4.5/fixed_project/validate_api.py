"""
API Validation Script
Tests all critical API scenarios manually
"""
import json
from src.app import app

# Create test client
client = app.test_client()

print("="*70)
print("MANUAL API VALIDATION TESTS")
print("="*70)

test_cases = [
    {
        "name": "Test 1: Health Check Endpoint",
        "method": "GET",
        "endpoint": "/health",
        "payload": None,
        "expected_status": 200
    },
    {
        "name": "Test 2: Normal Discount Calculation (100 * 0.8)",
        "method": "POST",
        "endpoint": "/api/coupons/calculate",
        "payload": {"original_price": 100, "discount_rate": 0.8},
        "expected_status": 200
    },
    {
        "name": "Test 3: Zero Discount Rate (Should return 400)",
        "method": "POST",
        "endpoint": "/api/coupons/calculate",
        "payload": {"original_price": 100, "discount_rate": 0},
        "expected_status": 400
    },
    {
        "name": "Test 4: Missing Required Parameter",
        "method": "POST",
        "endpoint": "/api/coupons/calculate",
        "payload": {"original_price": 100},
        "expected_status": 400
    },
    {
        "name": "Test 5: Invalid Type (String for price)",
        "method": "POST",
        "endpoint": "/api/coupons/calculate",
        "payload": {"original_price": "not_a_number", "discount_rate": 0.5},
        "expected_status": 400
    },
    {
        "name": "Test 6: Out of Range Discount Rate (> 1)",
        "method": "POST",
        "endpoint": "/api/coupons/calculate",
        "payload": {"original_price": 100, "discount_rate": 1.5},
        "expected_status": 400
    },
    {
        "name": "Test 7: Large Price Calculation",
        "method": "POST",
        "endpoint": "/api/coupons/calculate",
        "payload": {"original_price": 999.99, "discount_rate": 0.5},
        "expected_status": 200
    },
    {
        "name": "Test 8: Negative Discount Rate",
        "method": "POST",
        "endpoint": "/api/coupons/calculate",
        "payload": {"original_price": 100, "discount_rate": -0.2},
        "expected_status": 400
    },
    {
        "name": "Test 9: Boundary - Discount Rate = 1.0",
        "method": "POST",
        "endpoint": "/api/coupons/calculate",
        "payload": {"original_price": 100, "discount_rate": 1.0},
        "expected_status": 200
    },
    {
        "name": "Test 10: Decimal Prices",
        "method": "POST",
        "endpoint": "/api/coupons/calculate",
        "payload": {"original_price": 99.99, "discount_rate": 0.5},
        "expected_status": 200
    }
]

passed = 0
failed = 0

for idx, test in enumerate(test_cases, 1):
    print(f"\n{test['name']}")
    print("-" * 70)
    
    if test['method'] == "GET":
        response = client.get(test['endpoint'])
    else:
        response = client.post(
            test['endpoint'],
            data=json.dumps(test['payload']),
            content_type='application/json'
        )
    
    status_ok = response.status_code == test['expected_status']
    result = "✓ PASS" if status_ok else "✗ FAIL"
    
    if status_ok:
        passed += 1
    else:
        failed += 1
    
    print(f"  Endpoint: {test['endpoint']}")
    print(f"  Expected Status: {test['expected_status']}")
    print(f"  Actual Status: {response.status_code} {result}")
    
    data = json.loads(response.data)
    
    # Validate calculation for successful responses
    if test['method'] == "POST" and response.status_code == 200:
        original = data['original_price']
        rate = data['discount_rate']
        final = data['final_price']
        saved = data['saved_amount']
        
        # Verify calculation correctness
        expected_final = original * rate
        expected_saved = original - final
        
        calc_correct = abs(final - expected_final) < 0.001 and abs(saved - expected_saved) < 0.001
        calc_status = "✓" if calc_correct else "✗"
        
        print(f"  Calculation Verification: {calc_status}")
        print(f"    Original: ${original}, Rate: {rate}")
        print(f"    Final: ${final} (Expected: ${expected_final:.2f})")
        print(f"    Saved: ${saved} (Expected: ${expected_saved:.2f})")
    else:
        print(f"  Response Message: {data.get('error', 'N/A')}")

print("\n" + "="*70)
print("VALIDATION SUMMARY")
print("="*70)
print(f"Total Tests: {len(test_cases)}")
print(f"Passed: {passed} ✓")
print(f"Failed: {failed}")
print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
print("="*70)

if failed == 0:
    print("\n✓✓✓ ALL MANUAL VALIDATION TESTS PASSED ✓✓✓\n")
else:
    print(f"\n✗ {failed} test(s) failed\n")
