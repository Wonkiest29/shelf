import json
import jwt
import datetime
import yaml
import tools

from tools.mongo import get_mongo_client
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from bson import ObjectId
from fastapi.responses import JSONResponse

ph = PasswordHasher()

async def signin(data):
    username = data.get('username')
    password = data.get('password')
    client = await get_mongo_client()
    db = client['shelf']
    collection = db['accounts']
    user = await collection.find_one({"username": username})
    config = tools.read_cfg()
    token = config['SECRET_KEY']
    print(user)
    if user:
        ph.verify(user['password'], password)
        data = {
            "subid": str(user['_id']),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(data, token, algorithm="HS256")
        return {"token": token}
        # return data
    else:
        return {"error": "User not found"}
    
async def signup(data):
    username = data.get('username')
    password = data.get('password')
    client = await get_mongo_client()
    db = client['shelf']
    collection = db['accounts']
    user = await collection.find_one({"username": username})
    if user:
        return {"error": "User already exists"}
    else:
        hashed = ph.hash(password)
        await collection.insert_one({"username": username, "password": hashed, "role": "user"})
        return {"status": "OK"}

async def update_dashboard(data):

    config = tools.read_cfg()

    if config['demo'] == True:
        return {"error": "Demo mode is enabled you can't change this settings"}

    data = json.loads(data)
    dashboard = data.get('public')
    mongourl = data.get('mongourl')
    secret = data.get('secret')

    tools.jwt_veiryf(jwt)

    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    config['dashboard']['public'] = dashboard
    config['mongourl'] = mongourl
    config['SECRET_KEY'] = secret

    with open('config.yml', 'w') as file:
        yaml.safe_dump(config, file)

    return {"status": "OK"}

async def update_user(id, data, token):
    username = data.get('username')
    password = data.get('password')
    permissions = data.get('role')

    if username == "admin":
        return {"error": "You can't change this user"}
    if id == "677e4fa9e07a6de17f955efe":
        return {"error": "You can't change this user"}

    decoded_jwt = tools.jwt_verify(token)
    client = await get_mongo_client()
    db = client['shelf']
    collection = db['accounts']
    print(decoded_jwt["subid"])
    id_admin = decoded_jwt['subid']
    user = await collection.find_one({"_id": ObjectId(decoded_jwt["subid"])})
    print(user)
    if user:
        if 'admin' in user['role']:
            update_data = {}
            if username:
                update_data['username'] = username
            if password:
                update_data['password'] = ph.hash(password)
            if permissions:
                update_data['role'] = permissions

            await collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
            return {"status": "OK"}
        else:
            return {"error": "Insufficient permissions"}
    else:
        return {"error": "User not found"}
    
async def delete_user(userid, token):
    if token is None:
        return {"error": "No token provided"}, 401
    if userid == "677e4fa9e07a6de17f955efe":
        return {"error": "You can't change this user"}

    decoded_jwt = tools.jwt_verify(token)
    client = await get_mongo_client()
    db = client['shelf']
    collection = db['accounts']
    user = await collection.find_one({"_id": ObjectId(decoded_jwt['subid'])})
    if user:
        try:
            await collection.delete_one({"_id": ObjectId(userid)})
            return {"status": "OK"}
        except Exception as e:
            print(e)
            return {"error": "Failed to delete user"}
    else:
        return {"error": "Insufficient permissions or user not found"}



async def users(jwt):
    print(jwt)
    if not jwt:
        return JSONResponse(content={"error": "No token provided"}, status_code=401)
        
    # if 'error' in a:
        # return a, 401

    try:
        is_admin = await tools.is_admin(a['subid'])
    except KeyError:
        return {"error": "Invalid token structure"}, 401

    if not is_admin:
        return {"error": "Insufficient permissions"}, 403

    client = await get_mongo_client()
    db = client['shelf']
    collection = db['accounts']

    users_cursor = collection.find({}, {"_id": 1, "username": 1, "role": 1})
    users = []
    async for user in users_cursor:
        users.append({
            "_id": str(user["_id"]),
            "username": user["username"],
            "role": user["role"]
        })

    return users