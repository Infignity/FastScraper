'''model definition'''
from datetime import datetime
from typing import Literal, List
from beanie.odm.documents import Document
from beanie import PydanticObjectId
from pydantic import Field
from src.core.config import simple_pydantic_model_config


class TaskResult(Document):
    '''TaskResult '''

    class Settings:
        '''meta data defintion'''
        name = "task_results"
        use_state_management = True
    model_config = simple_pydantic_model_config
    id: PydanticObjectId = Field(
        description="Task result Id",
        default_factory=lambda: PydanticObjectId(),
        alias="_id"
    )
    task_id: PydanticObjectId
    first_name: str = None
    last_name: str = None
    linkedin_url: str = None
    organization_name: str = None
    department: str = None
    seniority: str = None
    industry: str = None
    headline: str = None
    keywords: str = None
    phone: str = None
    email: str = None
    domain: str = None
    company_address: str = None
    num_employee: str = None
    headline: str = None
    entity_id: str = None
    city: str = None
    state: str = None
    country: str = None
    person_linkedin: str = None
    company_linkedin: str = None
    landing_page_text: str = None
    company_name: str = None
    website: str = None
    apolo_email: str = None


class Task(Document):
    '''Task Defintions'''

    class Settings:
        '''meta data '''
        name = "tasks"
        use_state_management = True
        
    model_config = simple_pydantic_model_config
    id: PydanticObjectId = Field(
        description="Task Id",
        default_factory=lambda: PydanticObjectId(),
        alias="_id"
    )   
    celery_task_id: str = Field(default="")
    registered_at: datetime = Field(default_factory=datetime.now)
    state: Literal["completed", "running", "notstarted"] = Field(default="notstarted")
    results: List[TaskResult] = Field(default=[])
    scraped_urls: List = Field(default=[])
    