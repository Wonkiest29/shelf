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


def jwt_verify(token):
    config = read_cfg()
    try:
        return jwt.decode(token, config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    
async def is_admin(id):
    client = await get_mongo_client()
    db = client['auth']
    collection = db['users']
    user = await collection.find_one({"_id": id})
    if user:
        if 'admin' in user.get('role', []):
            return True
    return False

async def is_user(id):
    client = await get_mongo_client()
    db = client['auth']
    collection = db['users']
    user = await collection.find_one({"_id": id})
    if user:
        return True
    return False
