import json
import argparse
from datetime import datetime

# File path for data persistence
DATA_FILE = "tasks.json"


class Task:
    def __init__(self, task_id, title, description, priority, due_date, completed=False):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed
        }

    def from_dict(task_dict):
        return Task(
            task_dict["task_id"],
            task_dict["title"],
            task_dict["description"],
            task_dict["priority"],
            task_dict["due_date"],
            task_dict["completed"]
        )


def load_tasks():
    try:
        with open(DATA_FILE, "r") as file:
            tasks = json.load(file)
            return [Task.from_dict(task) for task in tasks]
    except FileNotFoundError:
        return []


def save_tasks(tasks):
    with open(DATA_FILE, "w") as file:
        json.dump([task.to_dict() for task in tasks], file, indent=2)


def add_task(title, description, priority, due_date):
    tasks = load_tasks()
    new_id = max([task.task_id for task in tasks], default=0) + 1
    new_task = Task(new_id, title, description, priority, due_date)
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{title}' added.")


def remove_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task.task_id != task_id]
    save_tasks(tasks)
    print(f"Task with ID {task_id} removed.")


def mark_task_completed(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task.task_id == task_id:
            task.completed = True
            break
    else:
        print(f"Task with ID {task_id} not found.")
        return
    save_tasks(tasks)
    print(f"Task with ID {task_id} marked as completed.")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        status = "Completed" if task.completed else "Pending"
        print(f"{task.task_id}. {task.title} - {task.description} [Priority: {task.priority}] [Due: {task.due_date}] [Status: {status}]")


def main():
    parser = argparse.ArgumentParser(description="Command-line To-Do List Application")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Title of the task")
    add_parser.add_argument("description", help="Description of the task")
    add_parser.add_argument("priority", choices=["high", "medium", "low"], help="Priority of the task")
    add_parser.add_argument("due_date", help="Due date of the task (YYYY-MM-DD)")

    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("task_id", type=int, help="ID of the task to remove")

    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to mark as completed")

    list_parser = subparsers.add_parser("list", help="List all tasks")

    args = parser.parse_args(args=[])


    if args.command == "add":
        try:
            due_date = datetime.strptime(args.due_date, "%Y-%m-%d").date()
            add_task(args.title, args.description, args.priority, str(due_date))
        except ValueError:
            print("Invalid due date format. Please use YYYY-MM-DD.")
    elif args.command == "remove":
        remove_task(args.task_id)
    elif args.command == "complete":
        mark_task_completed(args.task_id)
    elif args.command == "list":
        list_tasks()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
