from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from service.redis.manager import cache_manager

TASK_LIST_CACHE_KEY = "all_tasks_list_cache"
DEFAULT_CACHE_TTL = 60 

class TaskManager:
    def __init__(self, db, collection):
        self.db = db
        self.collection = collection
        self.cache = cache_manager 

    def _serialize(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task["_id"] = str(task["_id"])
        if isinstance(task.get("created_at"), datetime):
            task["created_at"] = task["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        return task

    def _invalidate_cache(self):
        self.cache.invalidate_cache(TASK_LIST_CACHE_KEY)

    def add_task(self, text: str, priority: int, completed: bool = False) -> Dict[str, Any]:
        task = {
            "text": text,
            "priority": priority,
            "completed": completed,
            "created_at": datetime.now(),
        }
        result = self.collection.insert_one(task)
        task["_id"] = str(result.inserted_id)
        self._invalidate_cache()
        
        return task

    def list_tasks(self, show_completed: Optional[bool] = None) -> List[Dict[str, Any]]:
        if show_completed is None and self.cache.is_connected():
            cached_data = self.cache.get_cache(TASK_LIST_CACHE_KEY)
            if cached_data:
                return cached_data

        query = {}
        if show_completed is not None:
            query["completed"] = show_completed
            
        tasks = list(self.collection.find(query).sort("created_at", -1))
        serialized_tasks = [self._serialize(t) for t in tasks]

        if show_completed is None and self.cache.is_connected():
            self.cache.set_cache(
                TASK_LIST_CACHE_KEY, 
                serialized_tasks, 
                ttl=DEFAULT_CACHE_TTL
            )
            
        return serialized_tasks

    def update_task(
        self,
        task_id: str,
        text: Optional[str] = None,
        priority: Optional[int] = None,
        completed: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        
        update_fields = {}
        if text is not None: update_fields["text"] = text
        if priority is not None: update_fields["priority"] = priority
        if completed is not None: update_fields["completed"] = completed

        if not update_fields: return None

        result = self.collection.find_one_and_update(
            {"_id": ObjectId(task_id)},
            {"$set": update_fields},
            return_document=True,
        )
        if result:
            self._invalidate_cache() 
            return self._serialize(result)
        return None

    def delete_task(self, task_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(task_id)})
        
        if result.deleted_count > 0:
            self._invalidate_cache()
            return True
        
        return False
    
    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        task = self.collection.find_one({"_id": ObjectId(task_id)})
        return self._serialize(task) if task else None