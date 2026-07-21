#!/usr/bin/env python3
"""
Task Manager CLI Tool

A command-line interface for managing tasks associated with users.
"""

import argparse
import sys
from models import Task, User


# Global data store for the CLI session
users = {}


def add_task(args):
    """
    Add a new task for a user.
    
    Args:
        args: Command-line arguments containing user and title
    """
    # Get or create the user
    if args.user not in users:
        users[args.user] = User(args.user)
        print(f"👤 Created new user: {args.user}")
    
    user = users[args.user]
    task = Task(args.title)
    user.add_task(task)


def complete_task(args):
    """
    Mark a task as completed for a user.
    
    Args:
        args: Command-line arguments containing user and title
    """
    user = users.get(args.user)
    if not user:
        print(f"❌ User '{args.user}' not found.")
        return
    
    task = user.get_task(args.title)
    if not task:
        print(f"❌ Task '{args.title}' not found for user '{args.user}'.")
        return
    
    # Mark the task as complete
    task.complete()


def list_tasks(args):
    """
    List tasks for a user.
    
    Args:
        args: Command-line arguments containing user and optional flags
    """
    user = users.get(args.user)
    if not user:
        print(f"❌ User '{args.user}' not found.")
        return
    
    # Get tasks based on completion status
    show_completed = getattr(args, 'all', False)
    tasks = user.list_tasks(show_completed)
    
    if not tasks:
        print(f"📭 No {'completed ' if show_completed else ''}tasks found for {args.user}.")
        return
    
    print(f"📋 Tasks for {args.user}:")
    for task_str in tasks:
        print(f"  {task_str}")


def delete_task(args):
    """
    Delete a task for a user.
    
    Args:
        args: Command-line arguments containing user and title
    """
    user = users.get(args.user)
    if not user:
        print(f"❌ User '{args.user}' not found.")
        return
    
    # Find and remove the task
    task_to_remove = None
    for task in user.tasks:
        if task.title == args.title:
            task_to_remove = task
            break
    
    if not task_to_remove:
        print(f"❌ Task '{args.title}' not found for user '{args.user}'.")
        return
    
    user.tasks.remove(task_to_remove)
    print(f"🗑️ Task '{args.title}' deleted for {args.user}.")


def main():
    """
    Main entry point for the CLI tool.
    """
    # Create the main parser
    parser = argparse.ArgumentParser(
        description="Task Manager CLI - Manage tasks for users",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_tool.py add-task Alice "Write unit tests"
  python cli_tool.py complete-task Alice "Write unit tests"
  python cli_tool.py list-tasks Alice
  python cli_tool.py list-tasks Alice --all
  python cli_tool.py delete-task Alice "Write unit tests"
        """
    )
    
    # Create subparsers for each command
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    subparsers.required = True
    
    # Add task command
    add_parser = subparsers.add_parser(
        'add-task',
        help='Add a new task for a user',
        description='Add a new task to a user\'s task list'
    )
    add_parser.add_argument(
        'user',
        help='Name of the user to add the task to'
    )
    add_parser.add_argument(
        'title',
        help='Title/description of the task'
    )
    add_parser.set_defaults(func=add_task)
    
    # Complete task command
    complete_parser = subparsers.add_parser(
        'complete-task',
        help='Mark a task as completed',
        description='Mark an existing task as completed for a user'
    )
    complete_parser.add_argument(
        'user',
        help='Name of the user who owns the task'
    )
    complete_parser.add_argument(
        'title',
        help='Title of the task to mark as completed'
    )
    complete_parser.set_defaults(func=complete_task)
    
    # List tasks command
    list_parser = subparsers.add_parser(
        'list-tasks',
        help='List tasks for a user',
        description='List all tasks or only incomplete tasks for a user'
    )
    list_parser.add_argument(
        'user',
        help='Name of the user whose tasks to list'
    )
    list_parser.add_argument(
        '--all',
        action='store_true',
        help='Show all tasks including completed ones'
    )
    list_parser.set_defaults(func=list_tasks)
    
    # Delete task command (extra functionality)
    delete_parser = subparsers.add_parser(
        'delete-task',
        help='Delete a task for a user',
        description='Remove a task from a user\'s task list'
    )
    delete_parser.add_argument(
        'user',
        help='Name of the user who owns the task'
    )
    delete_parser.add_argument(
        'title',
        help='Title of the task to delete'
    )
    delete_parser.set_defaults(func=delete_task)
    
    # Parse arguments and execute the appropriate function
    args = parser.parse_args()
    
    try:
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()