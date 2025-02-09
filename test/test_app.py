from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. Test functionality of post request
def test_process_receipt():
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
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 200
    assert "id" in response.json()

# 2. Test functionality of get request
def test_get_points():
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
    process_response = client.post("/receipts/process", json=receipt)
    receipt_id = process_response.json()["id"]

    response = client.get(f"/receipts/{receipt_id}/points")
    assert response.status_code == 200
    assert "points" in response.json()

# 3. Test for evaluating points
def test_evaluate_points():
    # Sample receipt input
    receipt_data = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"}
        ],
        "total": "9.00"
    }

    # Send receipt for processing
    response = client.post("/receipts/process", json=receipt_data)
    assert response.status_code == 200
    receipt_id = response.json().get("id")
    assert receipt_id is not None

    # Retrieve points for the given receipt ID
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    points = points_response.json().get("points")

    # Expected breakdown:
    # 50 points - total is a round dollar amount
    # 25 points - total is a multiple of 0.25
    # 14 points - retailer name has 14 alphanumeric characters
    # 10 points - purchase time is between 2:00pm and 4:00pm
    # 10 points - 4 items (2 pairs @ 5 points each)
    expected_points = 109
    assert points == expected_points, f"Expected {expected_points} but got {points}"

def test_target_receipt_points():
    # Sample Target receipt
    receipt_data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
        ],
        "total": "35.35"
    }

    # Send receipt for processing
    response = client.post("/receipts/process", json=receipt_data)
    assert response.status_code == 200
    receipt_id = response.json().get("id")
    assert receipt_id is not None

    # Retrieve points for the given receipt ID
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    points = points_response.json().get("points")

    # Expected breakdown:
    # 6 points - retailer name has 6 alphanumeric characters
    # 10 points - 5 items (2 pairs @ 5 points each)
    # 3 Points - "Emils Cheese Pizza" is 18 characters (a multiple of 3)
    #            item price of 12.25 * 0.2 = 2.45, rounded up is 3 points
    # 3 Points - "Klarbrunn 12-PK 12 FL OZ" is 24 characters (a multiple of 3)
    #            item price of 12.00 * 0.2 = 2.4, rounded up is 3 points
    # 6 points - purchase day is odd
    expected_points = 28

    assert points == expected_points, f"Expected {expected_points} but got {points}"

