"""Simple task management tools - Understand this first!"""
from typing import List, Dict, Optional
from datetime import datetime

class SimpleTaskManager:
    """A simple in-memory task manager"""
    
    def __init__(self):
        # Dictionary to store tasks: {task_id: task_data}
        self.tasks = {}
        self.task_counter = 0
        print("✅ Task Manager initialized")
    
    def create_task(self, title: str, description: str = "") -> Dict:
        """Create a new task - returns dictionary with task info"""
        task_id = f"task_{self.task_counter}"
        self.task_counter += 1
        
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "completed": False,
            "priority": "medium"
        }
        
        self.tasks[task_id] = task
        print(f"📝 Created task: {title} (ID: {task_id})")
        
        return {
            "status": "success",
            "task": task,
            "message": f"Task '{title}' created successfully"
        }
    
    def list_tasks(self, show_completed: bool = False) -> List[Dict]:
        """List all tasks - returns list of task dictionaries"""
        if not self.tasks:
            print("📭 No tasks found")
            return []
        
        filtered_tasks = []
        for task in self.tasks.values():
            if not show_completed and task["completed"]:
                continue
            filtered_tasks.append(task)
        
        print(f"📋 Found {len(filtered_tasks)} tasks")
        return filtered_tasks
    
    def complete_task(self, task_id: str) -> Dict:
        """Mark a task as completed"""
        if task_id not in self.tasks:
            return {"status": "error", "message": f"Task {task_id} not found"}
        
        self.tasks[task_id]["completed"] = True
        self.tasks[task_id]["completed_at"] = datetime.now().isoformat()
        
        print(f"✅ Completed task: {self.tasks[task_id]['title']}")
        return {
            "status": "success",
            "message": f"Task {task_id} marked as completed"
        }
    
    def delete_task(self, task_id: str) -> Dict:
        """Delete a task"""
        if task_id not in self.tasks:
            return {"status": "error", "message": f"Task {task_id} not found"}
        
        title = self.tasks[task_id]["title"]
        del self.tasks[task_id]
        
        print(f"🗑️ Deleted task: {title}")
        return {"status": "success", "message": f"Task '{title}' deleted"}
    
    def get_stats(self) -> Dict:
        """Get statistics about tasks"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks.values() if t["completed"])
        pending = total - completed
        
        return {
            "total_tasks": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": completed/total if total > 0 else 0
        }