from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.middlewares.auth_handle import authorization
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_services import TaskService

task_router = APIRouter()
task_service = TaskService()

@task_router.post("/",
                  dependencies=[Depends(authorization)], 
                  response_model=TaskResponse, 
                  status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """
    Create a new task
    """
    created_task = await task_service.create_task(task)
    return created_task

@task_router.get("/", dependencies=[Depends(authorization)],  response_model=List[TaskResponse])
async def get_all_tasks():
    """
    Get all tasks
    """
    tasks = await task_service.get_all_tasks()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No tasks found"
        )
    return tasks

@task_router.get("/{task_id}", dependencies=[Depends(authorization)],  response_model=TaskResponse)
async def get_task(task_id: str):
    """
    Get a specific task by ID
    """
    task = await task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task

@task_router.put("/{task_id}", dependencies=[Depends(authorization)],  response_model=TaskResponse)
async def update_task(task_id: str, task_data: TaskUpdate):
    """
    Update a task
    """
    updated_task = await task_service.update_task(task_id, task_data)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return updated_task

@task_router.delete("/{task_id}", dependencies=[Depends(authorization)],  status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    """
    Delete a task
    """
    deleted = await task_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return None