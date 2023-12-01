'''modules for website scrapper'''
import uuid
from io import BytesIO
from typing import List, Dict
from beanie import PydanticObjectId
import pandas as pd
from fastapi import (
    Body, APIRouter, Request, status, Response, 
    UploadFile, File, HTTPException
)
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from celery.result import AsyncResult
# define modules
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
    tasks_main = await Task.find().project(TaskView).to_list()
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
    csv_list: List[Dict[str, any]] = []
    try:
        csv_bytes = file.file.read()
        buffer = BytesIO(csv_bytes)
        print(buffer)
        csv_cls = PandasCsv()
        csv_list = csv_cls.read_csv_to_list(buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Something went wrong -> {e}')
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
    print(f"celery with the task id started: {task_result.id}")
    new_task.celery_task_id = task_result.id

    await new_task.create()
    response.status_code = status.HTTP_200_OK
    return new_task.model_dump(exclude=["results", "scraped_urls"])
    

@router.get("/tasks/{task_id}")
async def get_status(task_id):
    '''get task id'''
    respt = None
    task_result = AsyncResult(task_id)
    if task_result.status == "SUCCESS":
        resp = await Task.find_one({'celeryTaskId': task_id})
        respt = str(resp.id)

    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
        "result_id": respt if respt else None
    }
    return JSONResponse(result)


@router.get("/taskss")
async def all_tasks(
    request: Request,
    response: Response
):
    """ Get form page and results """
    tasks_main = await Task.find().project(TaskView).to_list()
    context = {"request": request, "tasks": tasks_main}
    response.status_code = status.HTTP_200_OK
    return templates.TemplateResponse("tasks.html", context)


@router.get("/specific-task/{task_id}")
async def query_specific_task(
    request: Request,
    task_id: str,
):
    '''specifics tasks'''
    tasks = await TaskResult.find(
        {"taskId": PydanticObjectId(task_id)}
    ).to_list()
    context = {
        "request": request,
        "data": tasks,
        "task_id": task_id
    }
    return templates.TemplateResponse("task.html", context)


@router.get("/success-task/{task_id}")
async def query_success_task(
    request: Request,
    task_id: str,
):
    '''specifics tasks'''
    tasks = await TaskResult.find(
        {"taskId": PydanticObjectId(task_id)}
    ).to_list()
    context = {
        "request": request,
        "data": tasks,
        "task_id": task_id
    }
    return templates.TemplateResponse("task.html", context)

@router.get("/download-csv/{task_id}")
async def download_csv(
    response: Response,
    task_id: str
):
    """ Download data as CSV """
    
    # Fetch data from MongoDB
    tasks_query = await TaskResult.find(
        {"taskId": PydanticObjectId(str(task_id))}
    ).to_list()
    tasks = [task.dict() for task in tasks_query]

    # Convert data to DataFrame
    df = pd.DataFrame(tasks)

    # Convert DataFrame to CSV
    csv_data = df.to_csv(index=False).encode("utf-8")

    # Generate a random UUID for the CSV file
    filename = f"{task_id}_{uuid.uuid4()}_tasks.csv"

    # Set response headers for download
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"
    
    # Return a StreamingResponse with CSV data
    return StreamingResponse(iter([csv_data]), media_type="text/csv")