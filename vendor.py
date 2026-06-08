from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter()

# ✅ 1. Get all vendor orders
@router.get("/vendor/orders")
def get_orders(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM orders ORDER BY created_at DESC"))
    return [dict(r._mapping) for r in result]


# ✅ 2. Accept Order
@router.post("/vendor/order/{id}/accept")
def accept_order(id: int, db: Session = Depends(get_db)):
    order = db.execute(text("SELECT * FROM orders WHERE id=:id"), {"id": id}).fetchone()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.execute(text("""
        UPDATE orders SET status='ACCEPTED'
        WHERE id=:id
    """), {"id": id})

    db.commit()
    return {"message": "Order accepted"}


# ✅ 3. Mark Preparing
@router.post("/vendor/order/{id}/preparing")
def preparing(id: int, db: Session = Depends(get_db)):
    db.execute(text("""
        UPDATE orders SET status='PREPARING'
        WHERE id=:id
    """), {"id": id})

    db.commit()
    return {"message": "Order preparing"}


# ✅ 4. Mark Ready + Create delivery (SAFE)
@router.post("/vendor/order/{id}/ready")
def ready(id: int, db: Session = Depends(get_db)):
    
    # ✅ Check order exists
    order = db.execute(text("SELECT * FROM orders WHERE id=:id"), {"id": id}).fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # ✅ Update order
    db.execute(text("""
        UPDATE orders SET status='READY'
        WHERE id=:id
    """), {"id": id})

    # ✅ Check delivery already exists
    delivery = db.execute(text("""
        SELECT * FROM deliveries WHERE order_id=:id
    """), {"id": id}).fetchone()

    if not delivery:
        db.execute(text("""
            INSERT INTO deliveries (order_id, status)
            VALUES (:id, 'READY_FOR_PICKUP')
        """), {"id": id})

    db.commit()

    return {"message": "Order READY, delivery created"}


# ✅ 5. Controlled status update (restricted)
@router.post("/vendor/order/{id}/status")
def update_status(id: int, status: str, db: Session = Depends(get_db)):

    allowed_status = ["ACCEPTED", "PREPARING", "READY"]

    if status not in allowed_status:
        raise HTTPException(status_code=400, detail="Invalid status")

    db.execute(text("""
        UPDATE orders SET status=:status WHERE id=:id
    """), {"status": status, "id": id})

    db.commit()

    return {"message": f"Order updated to {status}"}