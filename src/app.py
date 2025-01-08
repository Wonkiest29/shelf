import fastapi
import tools
import json

from pydantic import BaseModel
from typing import Optional

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None

app = fastapi.FastAPI()

@app.post("/signin/", tags=["account"])
async def login(data: dict):
    print(data)
    return await tools.signin(data)

@app.post("/signup/", tags=["account"])
async def register(data: dict):
    return await tools.signup(data)

@app.put("/settings/", tags=["account"])
async def update_settings(data: dict):
    return await tools.update_dashboard(data)

@app.get("/items/", tags=["items"])
async def get_items():
    return await tools.get_items()

@app.post("/items/", tags=["items"])
async def create_item(data: dict):
    return await tools.create_item(data)

@app.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: str):
    print(item_id)
    return await tools.get_item(item_id)

@app.put("/items/{item_id}", tags=["items"])
async def update_item(item_id: str, item_update: ItemUpdate):
    return await tools.update_item(item_id, item_update.dict(exclude_unset=True))

@app.delete("/items/{item_id}", tags=["items"])
async def delete_item(item_id: str):
    return await tools.delete_item(item_id)
