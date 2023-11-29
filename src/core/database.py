""" Includes code to communicate with mongodb database """

from typing import List
import motor.motor_asyncio
from beanie import init_beanie
from src.core.config import (
    mongo_url,
    db_name,
)


async def init_db(models: List):
    """
    Initializes the database connection using async motor driver
    :param models: A list of models to add
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
    await init_beanie(
        database=client.get_default_database(db_name), document_models=models
    )
    