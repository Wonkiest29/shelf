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
    # print(key)
    if not jwt_token:
        return {"error": "No token provided"}, 401
    try:
        decoded_token = jwt.decode(jwt_token, key, algorithms=["HS256"])
        # print(decoded_token)
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    

async def is_user(id, admin=None):
    client = await get_mongo_client()
    db = client['shelf']
    collection = db['accounts']
    try:
        user = await collection.find_one({"_id": ObjectId(id)})
        if not user:
            # print("User not found")
            return False

        if admin is True:
            if isinstance(user.get('role'), str) and 'admin' in user['role']:
                # print("User is admin")
                return True
            else:
                # print("User is not admin")
                return False

        # print("User found")
        return True
    except Exception as e:
        print(f"Error finding user: {e}")
        return False