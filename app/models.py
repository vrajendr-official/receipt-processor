from pydantic import BaseModel, Field, constr, ConfigDict
from typing import List
from datetime import date, time
from uuid import uuid4


class Item(BaseModel):
    shortDescription: constr(pattern=r"^[\w\s\-]+$") = Field(
        ..., description="The Short Product Description for the item."
    )
    price: constr(pattern=r"^\d+\.\d{2}$") = Field(
        ..., description="The total price paid for this item."
    )

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'shortDescription': 'Mountain Dew 12PK',
                'price': '6.49'
            }
        }
    )


class Receipt(BaseModel):
    retailer: constr(pattern=r"^[\w\s\-&]+$") = Field(
        ..., description="The name of the retailer or store the receipt is from."
    )
    purchaseDate: date = Field(
        ..., description="The date of the purchase printed on the receipt."
    )
    purchaseTime: time = Field(
        ..., description="The time of the purchase printed on the receipt (24-hour format)."
    )
    items: List[Item] = Field(
        ..., min_length=1, description="List of items in the receipt."
    )
    total: constr(pattern=r"^\d+\.\d{2}$") = Field(
        ..., description="The total amount paid on the receipt."
    )

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'retailer': 'M&M Corner Market',
                'purchaseDate': '2022-01-01',
                'purchaseTime': '13:01',
                'items': [
                    {'shortDescription': 'Mountain Dew 12PK', 'price': '6.49'}
                ],
                'total': '6.49'
            }
        }
    )


class ReceiptResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), pattern=r"^\S+$")

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'id': 'adb6b560-0eef-42bc-9d16-df48f30e89b2'
            }
        }
    )


class PointsResponse(BaseModel):
    points: int = Field(..., description="The number of points awarded.")

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'points': 100
            }
        }
    )