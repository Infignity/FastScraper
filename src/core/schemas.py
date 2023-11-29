''''''
from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from src.core.config import simple_pydantic_model_config


class TaskView(BaseModel):
    '''Task view model'''
    model_config = simple_pydantic_model_config
    id: PydanticObjectId = Field(alias="_id")
    celery_task_id: str
    registered_at: datetime
    state: Literal["completed", "running", "notstarted"]
