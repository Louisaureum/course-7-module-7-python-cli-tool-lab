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
        
        Returns:
            str: Confirmation message
        """
        self.completed = True
        message = f"✅ Task '{self.title}' completed."
        print(message)
        return message
    
    def __str__(self):
        """String representation of the task."""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.title}"


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
            
        Returns:
            str: Confirmation message
        """
        self.tasks.append(task)
        message = f"📌 Task '{task.title}' added to {self.name}."
        print(message)
        return message
    
    def get_task(self, title):
        """
        Find a task by its title.
        
        Args:
            title (str): The task title to find
            
        Returns:
            Task or None: The found task or None if not found
        """
        for task in self.tasks:
            if task.title == title:
                return task
        return None
    
    def list_tasks(self, show_completed=False):
        """
        List all tasks for the user.
        
        Args:
            show_completed (bool): Whether to show completed tasks
            
        Returns:
            list: List of task strings
        """
        tasks_to_show = self.tasks if show_completed else [t for t in self.tasks if not t.completed]
        return [str(task) for task in tasks_to_show]
    
    def __str__(self):
        """String representation of the user."""
        return f"User: {self.name} ({len(self.tasks)} tasks)"