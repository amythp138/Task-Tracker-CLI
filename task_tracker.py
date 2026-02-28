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
import argparse
from datetime import datetime


class TaskTracker:
    def __init__(self):
        self.task_file = os.path.join(os.path.dirname(__file__), 'tasks.json')

    def _ensure_task_file(self):
        """Create tasks.json with [] if it doesn't exist. Returns True on error."""
        if not os.path.exists(self.task_file):
            try:
                with open(self.task_file, "w") as f:
                    json.dump([], f)
            except OSError:
                return True
        return False

    def _load_tasks(self):
        """Load tasks from file. Returns (tasks_list, error_message)."""
        if self._ensure_task_file():
            return None, "Task file not found"
        try:
            with open(self.task_file, "r") as f:
                data = f.read().strip()
                tasks = json.loads(data) if data else []
            if not isinstance(tasks, list):
                tasks = []
            return tasks, None
        except json.JSONDecodeError:
            return [], None
        except Exception as e:
            return None, f"Error: {e}"

    def _save_tasks(self, tasks):
        with open(self.task_file, "w") as f:
            json.dump(tasks, f, indent=2)

    def _find_task(self, tasks, task_id):
        for i, t in enumerate(tasks):
            if t.get("id") == task_id:
                return i, t
        return -1, None

    def AddTask(self, task_desc):
        if task_desc is None or not str(task_desc).strip():
            return "Task description is required"
        task_dict = {
            "id": str(uuid.uuid4()),
            "description": task_desc.strip(),
            "status": "INPROGRESS",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        tasks, err = self._load_tasks()
        if err:
            return err
        tasks.append(task_dict)
        self._save_tasks(tasks)
        return "Task added successfully"

    def UpdateTask(self, task_id, task_desc):
        tasks, err = self._load_tasks()
        if err:
            return err
        idx, task = self._find_task(tasks, task_id)
        if idx < 0:
            return "Task not found"
        tasks[idx]["description"] = task_desc.strip()
        tasks[idx]["updated_at"] = datetime.now().isoformat()
        self._save_tasks(tasks)
        return "Task updated successfully"

    def DeleteTask(self, task_id):
        tasks, err = self._load_tasks()
        if err:
            return err
        idx, _ = self._find_task(tasks, task_id)
        if idx < 0:
            return "Task not found"
        tasks.pop(idx)
        self._save_tasks(tasks)
        return "Task deleted successfully"

    def MarkTaskAsInProgress(self, task_id):
        tasks, err = self._load_tasks()
        if err:
            return err
        idx, _ = self._find_task(tasks, task_id)
        if idx < 0:
            return "Task not found"
        tasks[idx]["status"] = "INPROGRESS"
        tasks[idx]["updated_at"] = datetime.now().isoformat()
        self._save_tasks(tasks)
        return "Task marked as in progress successfully"

    def MarkTaskAsDone(self, task_id):
        tasks, err = self._load_tasks()
        if err:
            return err
        idx, _ = self._find_task(tasks, task_id)
        if idx < 0:
            return "Task not found"
        tasks[idx]["status"] = "DONE"
        tasks[idx]["updated_at"] = datetime.now().isoformat()
        self._save_tasks(tasks)
        return "Task marked as done successfully"

    def ListTasksByStatus(self, status):
        tasks, err = self._load_tasks()
        if err:
            return err
        status_upper = (status or "").upper().replace("-", "")
        if status_upper in ("INPROGRESS", "IN_PROGRESS"):
            status_upper = "INPROGRESS"
        filtered = [t for t in tasks if t.get("status", "").upper() == status_upper]
        return filtered

    def ListAllTasks(self):
        tasks, err = self._load_tasks()
        if err:
            return err
        return tasks


def _format_task(t, short_id=False):
    tid = t.get("id", "")
    if short_id:
        tid = tid[:8] if len(tid) >= 8 else tid
    return f"  [{tid}] {t.get('description', '')}  ({t.get('status', '')})"


def _print_tasks(result):
    """Print task list or error message."""
    if isinstance(result, str):
        print(result)
    elif not result:
        print("No tasks.")
    else:
        for t in result:
            print(_format_task(t))


def run_interactive():
    """Interactive menu: prompt user for actions and input."""
    tracker = TaskTracker()
    status_choices = ["1", "2", "3", "4"]  # all, in-progress, done, todo

    while True:
        print("\n--- Task Tracker ---")
        print("1. Add task")
        print("2. List tasks")
        print("3. Update task")
        print("4. Delete task")
        print("5. Mark task in progress")
        print("6. Mark task done")
        print("7. Quit")
        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
            desc = input("Task description: ").strip()
            if not desc:
                print("Task description is required.")
                continue
            msg = tracker.AddTask(desc)
            print(msg)
            if "successfully" in msg:
                tasks, _ = tracker._load_tasks()
                if tasks:
                    print(_format_task(tasks[-1]))

        elif choice == "2":
            print("\nFilter by status: 1=All, 2=In progress, 3=Done, 4=Todo")
            status_choice = input("Filter (1-4) [default 1]: ").strip() or "1"
            if status_choice == "1":
                result = tracker.ListAllTasks()
            else:
                status_map = {"2": "INPROGRESS", "3": "DONE", "4": "TODO"}
                result = tracker.ListTasksByStatus(status_map.get(status_choice, ""))
            _print_tasks(result)

        elif choice == "3":
            task_id = input("Task ID (from list): ").strip()
            if not task_id:
                print("Task ID is required.")
                continue
            desc = input("New description: ").strip()
            if not desc:
                print("Description is required.")
                continue
            print(tracker.UpdateTask(task_id, desc))

        elif choice == "4":
            task_id = input("Task ID to delete: ").strip()
            if not task_id:
                print("Task ID is required.")
                continue
            print(tracker.DeleteTask(task_id))

        elif choice == "5":
            task_id = input("Task ID to mark in progress: ").strip()
            if not task_id:
                print("Task ID is required.")
                continue
            print(tracker.MarkTaskAsInProgress(task_id))

        elif choice == "6":
            task_id = input("Task ID to mark done: ").strip()
            if not task_id:
                print("Task ID is required.")
                continue
            print(tracker.MarkTaskAsDone(task_id))

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-7.")


def main():
    tracker = TaskTracker()
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode (prompt for input)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command (omit for interactive mode)")

    p_add = subparsers.add_parser("add", help="Add a new task")
    p_add.add_argument("description", help="Task description", nargs="?", default=None)

    p_list = subparsers.add_parser("list", help="List tasks (optionally by status)")
    p_list.add_argument("--status", "-s", choices=["todo", "in-progress", "done"], help="Filter by status")

    p_update = subparsers.add_parser("update", help="Update a task description")
    p_update.add_argument("task_id", help="Task ID (e.g. from list)")
    p_update.add_argument("description", help="New description")

    p_delete = subparsers.add_parser("delete", help="Delete a task")
    p_delete.add_argument("task_id", help="Task ID")

    p_ip = subparsers.add_parser("in-progress", help="Mark task as in progress")
    p_ip.add_argument("task_id", help="Task ID")

    p_done = subparsers.add_parser("done", help="Mark task as done")
    p_done.add_argument("task_id", help="Task ID")

    args = parser.parse_args()

    # No command and not --interactive: run interactive by default
    if args.command is None:
        run_interactive()
        return

    if args.command == "add":
        desc = args.description
        if desc is None:
            desc = input("Task description: ").strip()
        msg = tracker.AddTask(desc)
        print(msg)
        if "successfully" in msg:
            tasks, _ = tracker._load_tasks()
            if tasks:
                print(_format_task(tasks[-1]))
    elif args.command == "list":
        if getattr(args, "status", None):
            status_map = {"todo": "TODO", "in-progress": "INPROGRESS", "done": "DONE"}
            result = tracker.ListTasksByStatus(status_map.get(args.status, args.status))
        else:
            result = tracker.ListAllTasks()
        _print_tasks(result)
    elif args.command == "update":
        print(tracker.UpdateTask(args.task_id, args.description))
    elif args.command == "delete":
        print(tracker.DeleteTask(args.task_id))
    elif args.command == "in-progress":
        print(tracker.MarkTaskAsInProgress(args.task_id))
    elif args.command == "done":
        print(tracker.MarkTaskAsDone(args.task_id))


if __name__ == "__main__":
    main()