from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TaskStatus(str, Enum):
    TODO = "por hacer"
    IN_PROGRESS = "en progreso"
    COMPLETED = "completada"

class TaskBase(BaseModel):
    title: str = Field(..., max_length=100, min_length=1, examples=["Tarea de ejemplo", "Revisar el código"])
    description: str = Field(..., max_length=500, min_length=1, examples=["Descripción de la tarea", "Detalles sobre la tarea a realizar"])
    status: TaskStatus = Field(default=TaskStatus.TODO, description="Estado de la tarea")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100, min_length=1, examples=["Tarea actualizada", "Revisar el código actualizado"])
    description: Optional[str] = Field(None, max_length=500, min_length=1, examples=["Descripción actualizada de la tarea", "Detalles actualizados sobre la tarea a realizar"])
    status: Optional[TaskStatus] = Field(None, description="Estado actualizado de la tarea")

class TaskResponse(TaskBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }