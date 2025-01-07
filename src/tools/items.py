import json

import tools

async def get_items():
    client = await tools.get_mongo_client()
    config = tools.read_cfg()
    if config["dashboard"]["public"]:
        db = client['public_items']
        collection = db['items']
        items = []
        async for item in collection.find():
            items.append(item)
        return items
    else:
        return {"error": "Access denied"}

async def create_item(data):
    client = await tools.get_mongo_client()

    db = client['items']
    collection = db['items']
    await collection.insert_one(data)
    return {"status": "OK"}

async def update_item(data):
    client = await tools.get_mongo_client()
    db = client['items']
    collection = db['items']
    await collection.update_one({"_id": data['_id']}, {"$set": data})
    return {"status": "OK"}

async def delete_item(data):
    client = await tools.get_mongo_client()
    db = client['items']
    collection = db['items']
    await collection.delete_one({"_id": data['_id']})
    return {"status": "OK"}