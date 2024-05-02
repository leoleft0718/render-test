from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define your FastAPI app
app = FastAPI()

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "postgres://render_test_01_user:sUNhggwRTUVoG2vg2oARdSiNSc6fbBuy@dpg-copjr6v79t8c73fvhjig-a.oregon-postgres.render.com/render_test_01"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

# Pydantic model for input validation
class ItemCreate(BaseModel):
    name: str
    description: str

# Endpoint to create a new item
@app.post("/items/")
def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Endpoint to retrieve an item by ID
@app.get("/items/{item_id}")
def read_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
