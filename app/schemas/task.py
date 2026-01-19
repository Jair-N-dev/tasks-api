from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# Enums para validación
class TaskStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

# Schemas
class TaskBase(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=2000)
    prioridad: TaskPriorityEnum = TaskPriorityEnum.MEDIUM
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    team_id: int
    asignado_a: Optional[int] = None

class TaskUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=3, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=2000)
    estado: Optional[TaskStatusEnum] = None
    prioridad: Optional[TaskPriorityEnum] = None
    asignado_a: Optional[int] = None
    due_date: Optional[datetime] = None

class Task(TaskBase):
    id: int
    estado: TaskStatusEnum
    team_id: int
    asignado_a: Optional[int]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class TaskWithDetails(Task):
    """Task con detalles de team y usuario asignado"""
    team_nombre: Optional[str] = None
    asignado_nombre: Optional[str] = None
    asignado_email: Optional[str] = None