import json
import tools
import random

from bson import ObjectId
from bson.errors import InvalidId

async def get_items():
    client = await tools.get_mongo_client()
    config = tools.read_cfg()
    if config["dashboard"]["public"]:
        db = client['shelf']
        collection = db['shelf']
        items = []
        async for item in collection.find({}, {"_id": 1, "name": 1, "type": 1, "description": 1}):
            items.append({
                "id": str(item["_id"]),
                "name": item["name"],
                "type": item["type"],
                "description": item["description"]
            })
        return items
    else:
        return {"error": "Access denied"}


async def get_item(id_item):
    client = await tools.get_mongo_client()
    db = client['shelf']
    collection = db['shelf']
    try:
        item_id = ObjectId(id_item)
        # print(item_id)
    except InvalidId:
        return {"error": "Invalid item ID"}
    item = await collection.find_one({"_id": item_id})
    if item:
        item.pop('_id', None)  # Remove the _id field if needed
    return item

async def create_item(data):
    client = await tools.get_mongo_client()
    name = data.get('name')
    type_ = data.get('type')
    description = data.get('description')

    data = {
        "name": name,
        "type": type_,
        "description": description,
    }
    db = client['shelf']
    collection = db['shelf']
    await collection.insert_one(data)
    return {"status": "OK", "id": str(data['_id'])}

async def update_item(item_id: str, data: dict):
    client = await tools.get_mongo_client()
    db = client['shelf']
    collection = db['shelf']
    try:
        object_id = ObjectId(item_id)
        result = await collection.update_one({"_id": object_id}, {"$set": data})
        if result.modified_count == 1:
            return {"status": "OK"}
        else:
            return {"error": "Item not found or no changes made"}
    except InvalidId:
        return {"error": "Invalid item ID"}

async def delete_item(item_id: str):
    client = await tools.get_mongo_client()
    db = client['shelf']
    collection = db['shelf']
    try:
        object_id = ObjectId(item_id)
        result = await collection.delete_one({"_id": object_id})
        if result.deleted_count == 1:
            return {"status": "OK"}
        else:
            return {"error": "Item not found"}
    except InvalidId:
        return {"error": "Invalid item ID"}