import uuid

from fastapi.testclient import TestClient
from app.main import app
import pytest
from pydantic import ValidationError
from app.models import Receipt

client = TestClient(app)

# 1. Test for valid receipt
def test_submit_valid_receipt():
    valid_receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
        ],
        "total": "35.35"
    }
    response = client.post("/receipts/process", json=valid_receipt)
    assert response.status_code == 200
    assert "id" in response.json()  # ID should be returned in the response
    assert isinstance(response.json()["id"], str)  # ID should be a string

# 1. Test for missing required fields
def test_missing_required_fields():
    # Test Missing retailer
    response = {
        "purchaseDate": "2022-01-01",
        "purchaseTime": "14:30",
        "total": "35.35",
        "items": [
            {"shortDescription": "Test Item", "price": "5.00"}
        ]
    }
    with pytest.raises(ValidationError):
        Receipt(**response)

    # Test Missing purchaseDate
    response = {
        "retailer": "Target",
        "purchaseTime": "14:30",
        "total": "35.35",
        "items": [
            {"shortDescription": "Test Item", "price": "5.00"}
        ]
    }
    with pytest.raises(ValidationError):
        Receipt(**response)

    # Test Missing total
    response = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "14:30",
        "items": [
            {"shortDescription": "Test Item", "price": "5.00"}
        ]
    }
    with pytest.raises(ValidationError):
        Receipt(**response)


# 2. Test for invalid date and time format (strings)
def test_invalid_date_time_format():
    # Invalid date format
    response = {
        "retailer": "Target",
        "purchaseDate": "2022-13-01",
        "purchaseTime": "14:30",
        "total": "35.35",
        "items": [
            {"shortDescription": "Test Item", "price": "5.00"}
        ]
    }
    with pytest.raises(ValidationError):
        Receipt(**response)

    # Invalid time format
    response = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "25:30",
        "total": "35.35",
        "items": [
            {"shortDescription": "Test Item", "price": "5.00"}
        ]
    }
    with pytest.raises(ValidationError):
        Receipt(**response)

# 3. Test for missing items in the receipt
def test_missing_items():
    # Empty items list
    response = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "14:30",
        "total": "35.35",
        "items": []  # Items list cannot be empty
    }
    with pytest.raises(ValidationError):
        Receipt(**response)


# 4. Test for malformed receipt id & not found receipt id
def test_get_points():
    # Sample receipt to be processed
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
        ],
        "total": "35.35"
    }

    # First, POST the receipt
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 200
    receipt_id = response.json().get("id")


    # Then, GET the points for the processed receipt (valid case)
    response = client.get(f"/receipts/{receipt_id}/points")
    assert isinstance(response.json()["points"], int)  # Points should be an integer
    assert response.status_code == 200
    assert "points" in response.json()

    malformed_receipt_id = "1234"  # Malformed ID (not matching the generated ID)
    response = client.get(f"/receipts/{malformed_receipt_id}/points")
    assert response.status_code == 404  # Expecting a 404 error for malformed ID
    assert response.json() == {"detail": "No receipt found for that ID."}

    not_found_receipt_id = str(uuid.uuid4())
    response = client.get(f"/receipts/{not_found_receipt_id}/points")
    assert response.status_code == 404  # Expecting a 404 error for not found ID
    assert response.json() == {"detail": "No receipt found for that ID."}


# 5. Test response code and bad response
def test_missing_required_fields_response():
    receipt = {
        "retailer": "Target",  # Missing purchaseDate, purchaseTime, items, total
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.json()["detail"] == "The receipt is invalid."

# 6. Test for empty receipt
def test_submit_empty_receipt():
    empty_receipt = {}
    response = client.post("/receipts/process", json=empty_receipt)
    assert response.status_code == 400
    assert response.json()["detail"] == "The receipt is invalid."


# 7. Test for process response schema
def test_receipt_process_response_schema():
    valid_receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"}
        ],
        "total": "6.49"
    }
    response = client.post("/receipts/process", json=valid_receipt)
    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json
    assert isinstance(response_json["id"], str)


# 8. Test for non json receipt
def test_submit_non_json_receipt():
    invalid_content_type_receipt = '{"retailer": "Target", "purchaseDate": "2022-01-01", "purchaseTime": "13:01", "total": "6.49"}'
    response = client.post("/receipts/process", data=invalid_content_type_receipt)
    assert response.status_code == 400


# 9. Test for invalid item price
def test_invalid_item_price_format():
    invalid_price_receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49A"}  # Invalid price format
        ],
        "total": "6.49"
    }
    response = client.post("/receipts/process", json=invalid_price_receipt)
    assert response.status_code == 400
    assert response.json()["detail"] == "The receipt is invalid."


# 10. Stress test
def test_submit_large_number_of_items():
    large_receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"shortDescription": f"Item {i}", "price": "10.00"} for i in range(1000)],
        "total": "10000.00"
    }
    response = client.post("/receipts/process", json=large_receipt)
    assert response.status_code == 200
    assert "id" in response.json()  # ID should be returned


