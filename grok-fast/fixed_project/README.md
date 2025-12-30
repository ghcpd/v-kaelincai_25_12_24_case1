# Fixed Coupon Calculator Project

This is a fixed version of the Flask-based coupon calculator API. The original project had several bugs that have been resolved in this version.

## Features

- Calculate final price after discount
- Proper input validation
- Error handling with meaningful messages
- Health check endpoint

## Installation

1. Ensure you have Python 3.8+ installed.
2. Clone or download this project.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python src/app.py
```

The server will start on http://localhost:5000

## API Documentation

### POST /api/coupons/calculate

Calculate the discounted price.

**Request Body:**
```json
{
    "original_price": 100.0,
    "discount_rate": 0.8
}
```

**Response (Success):**
```json
{
    "original_price": 100.0,
    "discount_rate": 0.8,
    "final_price": 80.0,
    "saved_amount": 20.0
}
```

**Response (Error):**
```json
{
    "error": "Error message"
}
```

**Validation Rules:**
- `original_price`: Required, numeric
- `discount_rate`: Required, numeric, 0 < value <= 1

### GET /health

Health check endpoint.

**Response:**
```json
{
    "status": "ok"
}
```

## Running Tests

```bash
pytest tests/test_coupon.py -v
```

All tests should pass.