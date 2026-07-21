"""Core models for the CLI task management system."""

class Task:
    """Represents a task with a title and completion status."""
    
    def __init__(self, title):
        """
        Initialize a new task.
        
        Args:
            title (str): The title/description of the task
        """
        self.title = title
        self.completed = False

    def complete(self):
        """
        Mark the task as completed and print confirmation.
        """
        self.completed = True
        print(f"✅ Task '{self.title}' completed.")


class User:
    """Represents a user with a collection of tasks."""
    
    def __init__(self, name):
        """
        Initialize a new user.
        
        Args:
            name (str): The user's name
        """
        self.name = name
        self.tasks = []

    def add_task(self, task):
        """
        Add a task to the user's task list.
        
        Args:
            task (Task): The task to add
        """
        self.tasks.append(task)
        print(f"📌 Task '{task.title}' added to {self.name}.")