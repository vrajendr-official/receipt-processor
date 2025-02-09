from app.models import Receipt
from decimal import Decimal, ROUND_UP
from datetime import time

def calculate_points(receipt: Receipt) -> int:
    points = 0

    # 1. One point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in receipt.retailer)

    # Convert `total` from string to Decimal
    total_amount = Decimal(receipt.total)

    # 2. 50 points if the total is a round dollar amount (no cents)
    if total_amount % 1 == 0:
        points += 50

    # 3. 25 points if the total is a multiple of 0.25
    if total_amount % Decimal('0.25') == 0:
        points += 25

    # 4. 5 points for every two items
    points += (len(receipt.items) // 2) * 5

    # 5. Item description length multiple of 3 rule
    for item in receipt.items:
        description_length = len(item.shortDescription.strip())  # Remove leading/trailing spaces
        item_price = Decimal(item.price)  # Convert price from string to Decimal
        if description_length % 3 == 0:
            points += int((item_price * Decimal('0.2')).quantize(Decimal('1'), rounding=ROUND_UP))

    # 6. 6 points if the day of the purchase date is odd
    if receipt.purchaseDate.day % 2 == 1:
        points += 6

    # 7. 10 points if the purchase time is after 2:00pm and before 4:00pm
    if time(14, 0) < receipt.purchaseTime < time(16, 0):
        points += 10

    return points