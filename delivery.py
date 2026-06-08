from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter()

# ✅ 1. GET AVAILABLE JOBS
@router.get("/delivery/jobs")
def get_jobs(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT * 
        FROM deliveries 
        WHERE status='READY_FOR_PICKUP'
    """))

    return [dict(r._mapping) for r in result]


# ✅ 2. ACCEPT JOB
@router.post("/delivery/{id}/accept")
def accept_job(id: int, db: Session = Depends(get_db)):
    
    # Check job exists
    delivery = db.execute(
        text("SELECT * FROM deliveries WHERE id=:id"),
        {"id": id}
    ).fetchone()

    if not delivery:
        raise HTTPException(status_code=404, detail="Job not found")

    if delivery.status != "READY_FOR_PICKUP":
        raise HTTPException(status_code=400, detail="Job not available")

    # Assign agent (for now static = 1)
    db.execute(text("""
        UPDATE deliveries
        SET status='ASSIGNED', delivery_agent_id=1
        WHERE id=:id
    """), {"id": id})

    db.commit()
    return {"message": "Job accepted"}


# ✅ 3. PICKED UP
@router.post("/delivery/{id}/picked-up")
def picked_up(id: int, db: Session = Depends(get_db)):

    delivery = db.execute(
        text("SELECT * FROM deliveries WHERE id=:id"),
        {"id": id}
    ).fetchone()

    if not delivery:
        raise HTTPException(status_code=404, detail="Job not found")

    if delivery.status != "ASSIGNED":
        raise HTTPException(status_code=400, detail="Cannot pick up yet")

    db.execute(
        text("UPDATE deliveries SET status='PICKED_UP' WHERE id=:id"),
        {"id": id}
    )

    db.commit()
    return {"message": "Order picked up"}


# ✅ 4. DELIVERED
@router.post("/delivery/{id}/delivered")
def mark_delivered(id: int, db: Session = Depends(get_db)):

    delivery = db.execute(
        text("SELECT * FROM deliveries WHERE id=:id"),
        {"id": id}
    ).fetchone()

    if not delivery:
        raise HTTPException(status_code=404, detail="Job not found")

    if delivery.status != "PICKED_UP":
        raise HTTPException(status_code=400, detail="Cannot mark delivered")

    # Update delivery
    db.execute(
        text("UPDATE deliveries SET status='DELIVERED' WHERE id=:id"),
        {"id": id}
    )

    # Update related order
    db.execute(
        text("""
            UPDATE orders 
            SET status='DELIVERED' 
            WHERE id=:order_id
        """),
        {"order_id": delivery.order_id}
    )

    db.commit()
    return {"message": "Order delivered"}