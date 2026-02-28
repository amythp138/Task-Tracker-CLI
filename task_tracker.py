# Add, Update, and Delete tasks

# Mark a task as in progress or done

# List all tasks

# List all tasks that are done

# List all tasks that are not done

# List all tasks that are in progress


# id: A unique identifier for the task

# description: A short description of the task

# status: The status of the task (todo, in-progress, done)

# createdAt: The date and time when the task was created

# updatedAt: The date and time when the task was last updated

import os
import json
import uuid
from datetime import datetime
class TaskTracker:
    def __init__(self):
        self.task_file = os.path.join(os.path.dirname(__file__), 'tasks.json')

    def check_task_file(self):
        if not os.path.exists(self.task_file):
            with open(self.task_file,'w') as f:
                pass 
    
    def AddTask(self,task_desc):
        if task_desc is None:
            return "Task description is required"
        task_dict = {
                    "id":str(uuid.uuid4()),
                    "descriptiom":task_desc,
                    "status":"INPROGRESS",
                    "created_at":datetime.now().isoformat(),
                    "updated_at":datetime.now().isoformat()
                 }
        if self.check_task_file():
            return "Task file not found"
        try:
            with open(self.task_file,'r') as f:
                tasks = json.load(f)
            tasks.append(task_dict)
        except Exception as e:
            return f"Error adding task: {e}"
        return "Task added successfully"

    def UpadateTask(self,task_id,task_desc):
        if self.check_task_file():
            return "Task file not found"
        try:
            with open(self.task_file,'r') as f:
                tasks = json.load(f)
            if tasks.get(task_id):
                tasks[task_id]['descriptiom'] = task_desc
                tasks[task_id]['updated_at'] = datetime.now().isoformat()
                with open(self.task_file,'w') as f:
                    json.dump(tasks,f,indent=4)
                return "Task updated successfully"
            else:
                return "Task not found"
        except Exception as e:
            return f"Error updating task: {e}"

    def DeleteTask(self,task_id):
        if self.check_task_file():
            return "Task file not found"
        try:
            with open(self.task_file,'r') as f:
                tasks = json.load(f)
            if tasks.get(task_id):
                del tasks[task_id]
                with open(self.task_file,'w') as f:
                    json.dump(tasks,f,indent=4)
                return "Task deleted successfully"
            else:
                return "Task not found"
        except Exception as e:
            return f"Error deleting task: {e}"

    def MarkTaskAsInProgress(self,task_id):
        if self.check_task_file():
            return "Task file not found"
        try:
            with open(self.task_file,'r') as f:
                tasks = json.load(f)
            if tasks.get(task_id):
                tasks[task_id]['status'] = "INPROGRESS"
                with open(self.task_file,'w') as f:
                    json.dump(tasks,f,indent=4)
                return "Task marked as in progress successfully"
            else:
                return "Task not found"
        except Exception as e:
            return f"Error marking task as in progress: {e}"

    def MarkTaskAsDone(self,task_id):
        if self.check_task_file():
            return "Task file not found"
        try:
            with open(self.task_file,'r') as f:
                tasks = json.load(f)
            if tasks.get(task_id):
                tasks[task_id]['status'] = "DONE"
                with open(self.task_file,'w') as f:
                    json.dump(tasks,f,indent=4)
                return "Task marked as done successfully"
            else:
                return "Task not found"
        except Exception as e:
            return f"Error marking task as done: {e}"

    def ListTasksByStatus(self,status):
        if self.check_task_file():
            return "Task file not found"
        try:
            with open(self.task_file,'r') as f:
                tasks = json.load(f)
            return tasks
        except Exception as e:
            return f"Error listing tasks by status: {e}"

    def ListAllTasks(self):
        if self.check_task_file():
            return "Task file not found"
        try:
            with open(self.task_file,'r') as f:
                tasks = json.load(f)
            return tasks
        except Exception as e:
            return f"Error listing all tasks: {e}"