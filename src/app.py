import fastapi

app = fastapi.FastAPI()

@app.post("/signin/", tags=["account"])
async def login(data: dict):
    ...
    # return {"username": username}

@app.post("/signup/", tags=["account"])
async def register(data: dict):
    # return {"username": username}
    ...

@app.put("/settings/", tags=["account"])
async def update_settings(data: dict):
    ...
    # return settings

@app.get("/items/", tags=["items"])
async def get_items():
    return {"items": ["item1", "item2"]}

@app.post("/items/", tags=["items"])
async def create_item(data: dict):
    ...

@app.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.put("/items/{item_id}", tags=["items"])
async def update_item(item_id: int, data: dict):
    ...
    # return {"item_name": item.name, "item_id": item_id}

@app.delete("/items/{item_id}", tags=["items"])
async def delete_item(item_id: int):
    return {"item_id": item_id}


