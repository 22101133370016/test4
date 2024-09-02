from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory database to store data
db: Dict[int, dict] = {}

# Data model using Pydantic
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# GET method to retrieve all items
@app.get("/items/")
async def get_items():
    return db

# GET method to retrieve a specific item by ID
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id] 

# POST method to create a new item
@app.post("/items/")
async def create_item(item: Item):
    item_id = len(db) + 1
    db[item_id] = item.dict()
    return {"item_id": item_id, **item.dict()}

# PUT method to update an existing item
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = item.dict()
    return {"message": "Item updated successfully", "updated_item": db[item_id]}

# DELETE method to delete an existing item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return {"message": "Item deleted successfully"}