from fastapi import APIRouter, HTTPException

from depends.db import db_dep
from schemas.order import Order
from services.order_processing import process_order

router = APIRouter()


@router.get("/")
async def get_orders():
    # Mocked response for getting orders
    return {"orders": [{"id": 1, "item": "Door", "quantity": 2}]}


class LocalSession:
    pass


@router.post("/")
async def create_order(db: db_dep, order: Order):
    # Mocked response for creating an order
    if not order:
        raise HTTPException(status_code=400, detail="Invalid order data")
    result = await process_order(order=order, db=db)

    return {"message": "Order created successfully", "order": order, "processing_result": result}
