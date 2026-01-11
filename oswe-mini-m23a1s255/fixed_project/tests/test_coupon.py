"""Tests for the fixed Coupon Service."""
import json
import pytest
from src.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestCouponCalculate:
    def test_health_check(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["status"] == "ok"

    def test_normal_discount_calculation(self, client):
        payload = {"original_price": 100, "discount_rate": 0.8}
        resp = client.post(
            "/api/coupons/calculate",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["original_price"] == 100
        assert data["discount_rate"] == 0.8
        assert data["final_price"] == 80.0
        assert data["saved_amount"] == 20.0

    def test_discount_rate_one_returns_same_price(self, client):
        payload = {"original_price": 50, "discount_rate": 1}
        resp = client.post(
            "/api/coupons/calculate",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["final_price"] == 50.0
        assert data["saved_amount"] == 0.0

    def test_zero_discount_rate_causes_error(self, client):
        payload = {"original_price": 100, "discount_rate": 0}
        resp = client.post(
            "/api/coupons/calculate",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert "error" in data
        assert "discount_rate" in data["error"].lower()

    def test_missing_parameters(self, client):
        payload = {"original_price": 100}
        resp = client.post(
            "/api/coupons/calculate",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert "missing required parameter" in data["error"].lower()

    def test_negative_discount_rate(self, client):
        payload = {"original_price": 100, "discount_rate": -0.1}
        resp = client.post(
            "/api/coupons/calculate",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_non_numeric_inputs(self, client):
        payload = {"original_price": "one hundred", "discount_rate": "abc"}
        resp = client.post(
            "/api/coupons/calculate",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_original_price_zero_allowed(self, client):
        payload = {"original_price": 0, "discount_rate": 0.5}
        resp = client.post(
            "/api/coupons/calculate",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["final_price"] == 0.0
        assert data["saved_amount"] == 0.0
