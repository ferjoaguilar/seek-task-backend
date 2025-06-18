from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from app.database.mongodb_database import get_database
from app.schemas.task_schemas import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self):
        self.db = get_database()
        self.task_collection = self.db['tasks']
    
    async def create_task(self, task: TaskCreate) -> dict:
        task_dict = task.dict()
        task_dict["created_at"] = datetime.utcnow()
        result = await self.task_collection.insert_one(task_dict)
        created_task = await self.task_collection.find_one({"_id": result.inserted_id})
        created_task["id"] = str(created_task.pop("_id"))
        return created_task
    
    async def get_all_tasks(self) -> List[dict]:
        tasks = []
        cursor = self.task_collection.find({})
        async for document in cursor:
            document["id"] = str(document.pop("_id"))
            tasks.append(document)
        return tasks
    
    async def get_task_by_id(self, task_id: str) -> Optional[dict]:
        task = await self.task_collection.find_one({"_id": ObjectId(task_id)})
        if task:
            task["id"] = str(task.pop("_id"))
            return task
        return None
       
    
    async def update_task(self, task_id: str, task_data: TaskUpdate) -> Optional[dict]:
        task_dict = {k: v for k, v in task_data.dict().items() if v is not None}
        if task_dict:
            task_dict["updated_at"] = datetime.utcnow()
            await self.task_collection.update_one(
                {"_id": ObjectId(task_id)}, {"$set": task_dict}
            )
        
        updated_task = await self.get_task_by_id(task_id)
        return updated_task
    
    async def delete_task(self, task_id: str) -> bool:
        result = await self.task_collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0