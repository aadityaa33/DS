from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# ✅ Load .env file
load_dotenv()

# ✅ Read DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Debug (optional - you can remove later)
print("DATABASE_URL =", DATABASE_URL)

# ✅ Create DB engine
engine = create_engine(DATABASE_URL, echo=True)

# ✅ Session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# ✅ Base
Base = declarative_base()

# ✅ Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()