import motor.motor_asyncio

async def get_mongo_client():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
    return client
