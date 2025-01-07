import yaml
import jwt
import datetime

from src.tools.mongo import get_mongo_client

__all__ = ["get_mongo_client"]


def read_cfg():
    with open("config.yml", "r") as f:
        return yaml.safe_load(f)


def jwt_veiryf(jwt):
    config = read_cfg()
    try:
        return jwt.decode(config['SECRET_KEY'], algorithms=["HS256"])
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
        if 'admin' in user.get('permissions', []):
            return True
    return False
