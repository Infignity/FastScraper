'''celery workers modules'''
from typing import List, Dict
from src.helpers.scrapper import ScrapperHelper
from .app import celery_app


@celery_app.task(name="create_task")
def create_task(task_id: str, datalist: List[Dict[str, any]]):
    '''task intiator'''
    for entry in datalist:
        organization_website = entry.get('organization_website')
        if organization_website:
            print(f"Visiting {organization_website}")
            sch = ScrapperHelper()
            selen_ret = sch.selen(organization_website)
            if selen_ret:
                # save to data 
                print(selen_ret)
                pass

    return True
