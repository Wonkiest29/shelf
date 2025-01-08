import json
import jwt
import datetime
import yaml
import tools

from tools.mongo import get_mongo_client
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

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
    data = json.loads(data)
    username = data.get('username')
    password = data.get('password')
    client = await get_mongo_client()
    db = client['auth']
    collection = db['users']
    user = await collection.find_one({"username": username})
    if user:
        return {"error": "User already exists"}
    else:
        hashed = ph.hash(password)
        await collection.insert_one({"username": username, "password": hashed, "permissions": []})
        return {"status": "OK"}

async def update_dashboard(data):
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

async def update_user(data):
    data = json.loads(data)
    id_user = data.get('id')
    username = data.get('username')
    password = data.get('password')
    permissions = data.get('permissions')

    decoded_jwt = tools.jwt_veiryf(jwt)
    
    client = await get_mongo_client()
    db = client['shelf']
    collection = db['users']
    user = await collection.find_one({"_id": decoded_jwt['subid']})
    if user:
        if user['permissions'].count('admin') > 0:
            update_data = {}
            if username:
                update_data['username'] = username
            if password:
                update_data['password'] = ph.hash(password)
            if permissions:
                update_data['permissions'] = permissions

            await collection.update_one({"_id": id_user}, {"$set": update_data})
            return {"status": "OK"}
        else:
            return {"error": "Insufficient permissions"}
    else:
        return {"error": "User not found"}