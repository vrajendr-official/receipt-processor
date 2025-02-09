from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.models import Receipt, ReceiptResponse, PointsResponse
from app.points_calculator import calculate_points
from app.storage import receipts_db

app = FastAPI()

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom handler to return a 400 Bad Request instead of 422."""
    return JSONResponse(
        status_code=400,
        content={
            "detail": "The receipt is invalid.",
            "errors": exc.errors(),
        },
    )

@app.post("/receipts/process", response_model=ReceiptResponse)
def process_receipt(receipt: Receipt):
    """Submits a receipt and returns an ID."""
    receipt_response = ReceiptResponse()  # Auto-generate ID
    points = calculate_points(receipt)  # Compute points
    receipts_db[receipt_response.id] = points  # Store receipt data
    return {"id": receipt_response.id}

@app.get("/receipts/{id}/points", response_model=PointsResponse)
def get_points(id: str):
    """Returns the points awarded for the receipt."""
    if id not in receipts_db:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")
    return {"points": receipts_db[id]}