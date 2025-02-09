from app.models import Receipt, Item
from app.points_calculator import calculate_points

def create_receipt_from_response(response):
    """Helper function to convert dictionary to Receipt object."""
    return Receipt(
        retailer=response["retailer"],
        purchaseDate=response["purchaseDate"],
        purchaseTime=response["purchaseTime"],
        total=response["total"],
        items=[Item(**item) for item in response["items"]]
    )


# 1. Test for alphanumeric retailer name (sum of alphanumeric characters)
def test_alphanumeric_retailer_points():
    response = {
        "retailer": "M&M Market",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:01",
        "total": "10.38",
        "items": [
            {"shortDescription": "Item 12", "price": "5.00"}
        ]
    }

    receipt = create_receipt_from_response(response)
    assert calculate_points(receipt) == 8  # 8 points for retailer


# 2. Test if 50 points are awarded when the total is a round dollar amount
def test_round_dollar_points():
    response = {
        "retailer": "M&M Market",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:01",
        "total": "10.00",
        "items": [
            {"shortDescription": "Item 12", "price": "5.00"}
        ]
    }

    receipt = create_receipt_from_response(response)
    assert calculate_points(receipt) == 83  # 50 points for round dollar, 8 points for retailer, 25 points for 0.25


# 3. Test if 25 points are awarded for total being a multiple of 0.25
def test_multiple_of_0_25_points():
    response = {
        "retailer": "M&M Market",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:01",
        "total": "10.25",
        "items": [
            {"shortDescription": "Item 12", "price": "5.00"}
        ]
    }

    receipt = create_receipt_from_response(response)
    assert calculate_points(receipt) == 33  # 25 points for multiple of 0.25, 8 points for retailer


# 4. Test for items with description length multiple of 3
def test_item_description_length_multiple_of_3():
    response = {
        "retailer": "M&M Market",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:01",
        "total": "10.38",
        "items": [
            {"shortDescription": "Item 1", "price": "5.00"}
        ]
    }

    receipt = create_receipt_from_response(response)
    assert calculate_points(receipt) == 9  # 8 points for retailer, 2 for item description points


# 5. Test if 6 points are awarded when the purchase day is odd
def test_purchase_day_odd():
    response = {
        "retailer": "M&M Market",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "total": "10.38",
        "items": [
            {"shortDescription": "Item 12", "price": "5.00"}
        ]
    }

    receipt = create_receipt_from_response(response)
    assert calculate_points(receipt) == 14  # 8 points for retailer, 6 points for odd day


# 6. Test if points are awarded for purchases made between 2pm and 4pm
def test_purchase_time_between_2_and_4pm():
    response = {
        "retailer": "M&M Market",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "14:01",
        "total": "10.38",
        "items": [
            {"shortDescription": "Item 12", "price": "5.00"}
        ]
    }

    receipt = create_receipt_from_response(response)
    assert calculate_points(receipt) == 18  # 10 points for time range, 8 points for retailer


# 7. Test when the receipt has more than one item
def test_single_item_receipt():
    response = {
        "retailer": "M&M Market",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:01",
        "total": "10.38",
        "items": [
            {"shortDescription": "Item 12", "price": "5.00"},
            {"shortDescription": "Item 23", "price": "5.00"}
        ]
    }

    receipt = create_receipt_from_response(response)
    assert calculate_points(receipt) == 13  # 8 points for retailer, 5 points for two items on the receipt