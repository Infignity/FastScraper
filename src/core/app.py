'''modules for website scrapper'''
from io import BytesIO
from typing import List, Dict
from fastapi import (
    Body, APIRouter, Request, status, Response, 
    UploadFile, File, HTTPException
)
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
# define modules
from celery.result import AsyncResult
from src.celery.worker import create_task
from src.core.models import Task, TaskResult
from src.core.schemas import TaskView
from src.helpers.pandas_csv import PandasCsv

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/test")
def entry():
    '''test app set up'''
    return {"Hello": "World"}


@router.get("/")
async def get_tasks(
    request: Request,
    response: Response
):
    """ Get form page and results """
    # tasks = await TaskResult.find().project(TaskView).to_list()
    tasks_main = await Task.find().project(TaskView).to_list()
    # tasks = await TaskResult.find().fetch_all()
    # tasks = await TaskResult.find().to_list()
    # tasks = [task.dict() for task in tasks]
    # print("TASKS: ", tasks_main)
    context = {"request": request, "tasks": []}
    response.status_code = status.HTTP_200_OK
    return templates.TemplateResponse("index.html", context)


@router.post("/tasks", status_code=201)
async def test(payload=Body(...)):
    '''Task func'''
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@router.post('/scrape')
async def scrap_task(
    request: Request, 
    response: Response,
    file: UploadFile = File(...)
):
    """ Register new scraping task """
    print("i was called")
    csv_list: List[Dict[str, any]] = []
    try:
        csv_bytes = file.file.read()
        buffer = BytesIO(csv_bytes)
        print(buffer)
        csv_cls = PandasCsv()
        csv_list = csv_cls.read_csv_to_list(buffer)
        print(csv_list)
    except:
        raise HTTPException(status_code=500, detail='Something went wrong')
    finally:
        # closing both the file and the buffer 
        buffer.close()
        file.file.close()

    new_task = Task()
    
    # trigger task
    task_result = create_task.delay(
        str(new_task.id),
        csv_list
    )
    new_task.celery_task_id = task_result.id
    await new_task.create()

    return JSONResponse({"task_id": task_result.id})
    


@router.get("/tasks/{task_id}")
def get_status(task_id):
    '''get task id'''
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
