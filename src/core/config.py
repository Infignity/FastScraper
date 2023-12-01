"""config file"""
import os
import random
from dotenv import load_dotenv
from pydantic import ConfigDict
from src.core.agents import agents

BASE_DIR = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1])
print(BASE_DIR)
# load config
load_dotenv()


mongo_url = os.getenv("MONGODB_CONN_STRING")
db_name = os.getenv("MONGODB_DB_NAME")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")


def to_camel_case(snake_str: str):
    """
    Converts a string in snake case to camel case
    :param snake_str: A string in snake case
    :return: A string in camel case
    """

    components = snake_str.split("_")
    components = [components[0]] + [x.capitalize() for x in components[1:]]
    camel_case_str = "".join(components)
    return camel_case_str


simple_pydantic_model_config = ConfigDict(
    str_strip_whitespace=True,
    use_enum_values=True,
    alias_generator=to_camel_case,
    populate_by_name=True
)


def get_random_ua():
    '''get random user agents'''
    return random.choice(agents)
