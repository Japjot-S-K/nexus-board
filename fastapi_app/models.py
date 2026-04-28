from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Status(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Priority = Priority.medium
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    due_date: Optional[str] = None