'''celery workers modules'''
import asyncio
from typing import List, Dict
from src.helpers.async_scraper import run
from .app import celery_app


@celery_app.task(name="run_crawler")
def create_task(task_id: str, datalist: List[Dict[str, any]]):
    """ Crawler function """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(task_id, datalist))
    
    return True


# @celery_app.task(name="create_task")
# def create_task(task_id: str, datalist: List[Dict[str, any]]):
#     '''task intiator'''
#     for entry in datalist:
#         organization_website = entry.get('organization_website')
#         if organization_website:
#             print(f"Visiting {organization_website}")
#             sch = ScrapperHelper()
#             selen_ret = sch.selen(organization_website)
#             if selen_ret:
#                 # save to data 
#                 print(selen_ret)
#                 pass

#     return True
