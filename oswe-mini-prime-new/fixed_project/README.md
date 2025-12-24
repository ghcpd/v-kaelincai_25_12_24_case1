# Fixed Coupon Service

This is the fixed version of the coupon calculation service.

## What was fixed
- Input validation for required parameters
- Division-by-zero handled (returns 400)
- Corrected business logic (multiplication instead of division)
- Range validation for `discount_rate` (0 < discount_rate <= 1)
- Type checks for numeric input
- Unified error responses in JSON

## Run locally
1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
2. Run the app:
   ```powershell
   python src/app.py
   ```

## API
POST /api/coupons/calculate
- Body: JSON {"original_price": <number>, "discount_rate": <number>}
- Success: 200 JSON {original_price, discount_rate, final_price, saved_amount}
- Errors: 400 with JSON {"error": "..."}

## Tests
Run:
```powershell
pytest tests/test_coupon.py -v
```
