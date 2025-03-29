from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from depends.db import get_db
from services.order_processing import process_order

from schemas.order import Order

router = APIRouter()

@router.get("/")
async def get_orders():
    # Mocked response for getting orders
    return {"orders": [{"id": 1, "item": "Door", "quantity": 2}]}


class LocalSession:
    pass


@router.post("/")
async def create_order(order: Order, db: Session = Depends(get_db)):
    # Mocked response for creating an order
    if not order:
        raise HTTPException(status_code=400, detail="Invalid order data")
    result = process_order(order=order, db=db)
    
    return {"message": "Order created successfully", "order": order, "processing_result": result}