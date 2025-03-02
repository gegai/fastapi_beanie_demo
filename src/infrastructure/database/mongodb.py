from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.infrastructure.config.settings import settings
from src.domain.entities.user import User
from src.domain.entities.scenes import Scene


async def init_db():
    client = AsyncIOMotorClient(settings.mongodb_url)
    await init_beanie(
        database=client[settings.database_name],
        document_models=[User, Scene]
    )
