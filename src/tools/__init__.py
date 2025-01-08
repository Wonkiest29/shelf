import yaml
import jwt
import datetime

from tools.mongo import get_mongo_client
from tools.items import *
from tools.accmgr import *

__all__ = ["get_mongo_client", "read_cfg", "jwt_verify", "is_admin", "get_items", "create_item", "update_item", "delete_item", "signin", "signup", "update_dashboard", "update_user"]


def read_cfg():
    with open("config.yml", "r") as f:
        return yaml.safe_load(f)


def jwt_verify(jwt_token):
    config = read_cfg()
    key = config["SECRET_KEY"]
    if not jwt_token:
        return {"error": "No token provided"}, 401
    # print(jwt_token)
    try:
        return jwt.decode(jwt_token, key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    
from bson import ObjectId

async def is_admin(id):
    client = await get_mongo_client()
    db = client['shelf']
    collection = db['accounts']
    try:
        user = await collection.find_one({"_id": ObjectId(id)})
    except Exception as e:
        print(f"Error finding user: {e}")
        return False

    print(user)
    if user and isinstance(user.get('role'), str):
        if 'admin' in user['role']:
            print("User is admin")
            return True
    print("User is not admin")
    return False

async def is_user(id):
    client = await get_mongo_client()
    db = client['auth']
    collection = db['users']
    user = await collection.find_one({"_id": id})
    if user:
        return True
    return False
