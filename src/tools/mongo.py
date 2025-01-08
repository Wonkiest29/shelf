import motor.motor_asyncio
import tools

async def get_mongo_client():
    config = tools.read_cfg()
    url = config['mongourl']
    collection_name = config['collection']
    client = motor.motor_asyncio.AsyncIOMotorClient(url)
    return client
