from fastapi import APIRouter, HTTPException
from .database import task_collection
from .models import TaskCreate, TaskUpdate
from bson import ObjectId
from datetime import datetime

router = APIRouter()

def task_serializer(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task.get("description", ""),
        "priority": task["priority"],
        "status": task["status"],
        "created_at": task.get("created_at", ""),
        "due_date": task.get("due_date", None),
    }

@router.get("/tasks")
async def get_tasks(search: str = None, priority: str = None, status: str = None):
    query = {}
    if search:
        query["title"] = {"$regex": search, "$options": "i"}
    if priority:
        query["priority"] = priority
    if status:
        query["status"] = status
    tasks = []
    async for task in task_collection.find(query):
        tasks.append(task_serializer(task))
    return tasks

@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = await task_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_serializer(task)

@router.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
    new_task = {
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "status": "todo",
        "created_at": datetime.utcnow().isoformat(),
        "due_date": task.due_date,
    }
    result = await task_collection.insert_one(new_task)
    created = await task_collection.find_one({"_id": result.inserted_id})
    return task_serializer(created)

@router.patch("/tasks/{task_id}")
async def update_task(task_id: str, update: TaskUpdate):
    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = await task_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = await task_collection.find_one({"_id": ObjectId(task_id)})
    return task_serializer(updated)

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    result = await task_collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}