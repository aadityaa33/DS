from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter()

@router.get("/products/nearby")
def get_products(lat: float, lng: float, db: Session = Depends(get_db)):
    query = text("""
        SELECT p.id, p.name, p.price, v.name as vendor_name,
        (
            6371 * acos(
                cos(radians(:lat)) *
                cos(radians(v.latitude)) *
                cos(radians(v.longitude) - radians(:lng)) +
                sin(radians(:lat)) *
                sin(radians(v.latitude))
            )
        ) AS distance
        FROM products p
        JOIN vendors v ON p.vendor_id = v.id
        ORDER BY distance
    """)

    result = db.execute(query, {"lat": lat, "lng": lng})
    return [dict(r._mapping) for r in result]