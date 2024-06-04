from pydantic import BaseModel
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database URL
DATABASE_URL = "sqlite:///./test.db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

# Initialize FastAPI
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


# Create the database tables
Base.metadata.create_all(bind=engine)


class ItemCreate(BaseModel):
    name: str
    description: str


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/items/", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    logger.info("Reading all items")
    try:
        db_items = db.query(Item).all()
        return db_items
    except Exception as e:
        logger.error(f"Error reading items: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    logger.info("Creating a new item")
    try:
        db_item = Item(name=item.name, description=item.description)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    logger.info(f"Reading item with ID {item_id}")
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if db_item is None:
            logger.warning(f"Item with ID {item_id} not found")
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item
    except Exception as e:
        logger.error(f"Error reading item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    logger.info(f"Updating item with ID {item_id}")
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if db_item is None:
            logger.warning(f"Item with ID {item_id} not found")
            raise HTTPException(status_code=404, detail="Item not found")
        db_item.name = item.name
        db_item.description = item.description
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        logger.error(f"Error updating item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting item with ID {item_id}")
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if db_item is None:
            logger.warning(f"Item with ID {item_id} not found")
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(db_item)
        db.commit()
        return {"detail": "Item deleted"}
    except Exception as e:
        logger.error(f"Error deleting item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
