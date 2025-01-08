import fastapi
import tools
import json

from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse



app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods, including OPTIONS
    allow_headers=["*"],
)

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

def extract_token(request: fastapi.Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        # print(auth_header)
        token = auth_header[len("Bearer "):]
        if token.lower() == "null":
            return False
        return token
    return 


@app.post("/signin/", tags=["account"])
async def login(data: dict):
    return await tools.signin(data)

@app.post("/signup/", tags=["account"])
async def register(data: dict):
    return await tools.signup(data)

@app.post("/signup/admin", tags=["account"])
async def register_admin(data: dict):
    return await tools.signup(data)

@app.get("/users/", tags=["account"])
async def get_users(request: fastapi.Request):
    token = extract_token(request)
    # if not token:
        # return JSONResponse(content={"error": "No token provided"}, status_code=401)
    return await tools.users(token)

@app.put("/users/{id}", tags=["account"])
async def update_user(id: str, data: UserUpdate, request: fastapi.Request):
    
    token = extract_token(request)
    return await tools.update_user(id, data.dict(exclude_unset=True), token)

@app.delete("/users/{user_id}", tags=["account"])
async def delete_user(user_id: str, token: str = fastapi.Depends(extract_token)):
    return await tools.delete_user(user_id, token)


@app.put("/settings/", tags=["account"])
async def update_settings(data: dict):
    return await tools.update_dashboard(data)

@app.delete("/deletedb/", tags=["account"])
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
    # print(item_id)
    return await tools.get_item(item_id)

@app.put("/items/{item_id}", tags=["items"])
async def update_item(item_id: str, item_update: ItemUpdate):
    return await tools.update_item(item_id, item_update.dict(exclude_unset=True))

@app.delete("/items/{item_id}", tags=["items"])
async def delete_item(item_id: str):
    return await tools.delete_item(item_id)
