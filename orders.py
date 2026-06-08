from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter()

# ✅ -------------------------------
# CREATE ORDER
# ✅ -------------------------------
@router.post("/order")
async def create_order(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()

        if "vendor_id" not in data or "items" not in data:
            raise HTTPException(400, "vendor_id and items required")

        user_id = data.get("user_id", 1)
        vendor_id = data["vendor_id"]
        items = data["items"]

        if not items:
            raise HTTPException(400, "Cart is empty")

        # ✅ Create order
        result = db.execute(text("""
            INSERT INTO orders (user_id, vendor_id, status)
            VALUES (:user_id, :vendor_id, 'PLACED')
            RETURNING id
        """), {
            "user_id": user_id,
            "vendor_id": vendor_id
        })

        order_id = result.fetchone()[0]

        # ✅ Insert items
        for item in items:
            db.execute(text("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (:order_id, :product_id, :qty, :price)
            """), {
                "order_id": order_id,
                "product_id": item["id"],
                "qty": item.get("quantity", 1),
                "price": item["price"]
            })

        db.commit()

        return {"message": "✅ Order created", "order_id": order_id}

    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))


# ✅ -------------------------------
# GET ALL ORDERS (Grouped)
# ✅ -------------------------------
@router.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT 
            o.id AS order_id,
            o.status,
            o.vendor_id,
            oi.product_id,
            oi.quantity,
            oi.price
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id
        ORDER BY o.id DESC
    """))

    orders = {}

    for row in result:
        row = dict(row._mapping)
        order_id = row["order_id"]

        if order_id not in orders:
            orders[order_id] = {
                "order_id": order_id,
                "status": row["status"],
                "vendor_id": row["vendor_id"],
                "items": []
            }

        if row["product_id"]:
            orders[order_id]["items"].append({
                "product_id": row["product_id"],
                "quantity": row["quantity"],
                "price": row["price"]
            })

    return list(orders.values())


# ✅ -------------------------------
# GET ORDER STATUS
# ✅ -------------------------------
@router.get("/orders/{id}/status")
def order_status(id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT status FROM orders WHERE id=:id"),
        {"id": id}
    ).fetchone()

    if not result:
        raise HTTPException(404, "Order not found")

    return {"order_id": id, "status": result[0]}


# ✅ -------------------------------
# UPDATE STATUS (Vendor / Delivery)
# ✅ -------------------------------
@router.put("/orders/{id}/status")
def update_status(id: int, status: str, db: Session = Depends(get_db)):

    valid_status = [
        "PLACED",
        "ACCEPTED",
        "PREPARING",
        "READY",
        "ASSIGNED",
        "PICKED",
        "DELIVERED"
    ]

    if status not in valid_status:
        raise HTTPException(400, "Invalid status")

    db.execute(
        text("UPDATE orders SET status=:status WHERE id=:id"),
        {"status": status, "id": id}
    )

    db.commit()

    return {"message": f"✅ Order {id} updated to {status}"}


# ✅ -------------------------------
# ASSIGN DELIVERY AGENT
# ✅ -------------------------------
@router.post("/assign-delivery/{order_id}")
def assign_delivery(order_id: int, db: Session = Depends(get_db)):

    agent = db.execute(text("""
        SELECT id FROM delivery_agents 
        WHERE available = true 
        LIMIT 1
    """)).fetchone()

    if not agent:
        raise HTTPException(400, "No delivery agent available")

    db.execute(text("""
        INSERT INTO deliveries (order_id, agent_id, status)
        VALUES (:order_id, :agent_id, 'ASSIGNED')
    """), {
        "order_id": order_id,
        "agent_id": agent[0]
    })

    # ✅ Update order status also
    db.execute(text("""
        UPDATE orders SET status='ASSIGNED' WHERE id=:id
    """), {"id": order_id})

    db.commit()

    return {
        "message": "✅ Delivery assigned",
        "agent_id": agent[0]
    }