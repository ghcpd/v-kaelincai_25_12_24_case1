# Fixed Coupon Calculator Service

This repository contains a fixed version of the coupon calculation Flask service. The original project had bugs (division-by-zero, missing validation, incorrect business logic). This version addresses those issues and adds comprehensive tests.

## Features
- Input validation (existence, numeric types)
- Range validation for `discount_rate` (0 &lt; discount_rate &le; 1)
- Correct business logic: `final_price = original_price * discount_rate`
- Unified error handling with clear JSON error messages
- Comprehensive tests covering edge cases

## Installation

1. Create and activate a virtual environment (recommended):

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows PowerShell

2. Install dependencies:

   pip install -r requirements.txt

## Running

Start the service:

   python src/app.py

Health check: GET /health

Calculate coupon: POST /api/coupons/calculate with JSON body:
{
  "original_price": 100,
  "discount_rate": 0.8
}

## Testing

Run the unit tests:

   pytest tests/test_coupon.py -v

## Behavior notes
- `discount_rate = 0` → 400 with message `discount_rate cannot be zero`
- Missing or non-numeric parameters → 400 with descriptive message
- Negative or >1 discount rates → 400 with message indicating valid range
