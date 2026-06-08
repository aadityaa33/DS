from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.database import Base, engine

# import routes
from app.routes import products, orders, vendor, delivery

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Create tables automatically
Base.metadata.create_all(bind=engine)

# ✅ Add routes
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(vendor.router)
app.include_router(delivery.router)

@app.get("/")
def home():
    return {"message": "Backend running ✅"}