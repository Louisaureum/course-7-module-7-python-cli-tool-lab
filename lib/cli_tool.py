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
    if user:
        for task in user.tasks:
            if task.title == args.title:
                task.complete()
                return
        print("❌ Task not found.")
    else:
        print("❌ User not found.")


def main():
    """
    Main entry point for the CLI tool.
    """
    # Create the main parser
    parser = argparse.ArgumentParser(
        description="Task Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create subparsers for each command
    subparsers = parser.add_subparsers(dest='command')
    
    # Add task command
    add_parser = subparsers.add_parser(
        'add-task',
        help='Add a new task'
    )
    add_parser.add_argument(
        'user',
        help='Name of the user'
    )
    add_parser.add_argument(
        'title',
        help='Title of the task'
    )
    add_parser.set_defaults(func=add_task)
    
    # Complete task command
    complete_parser = subparsers.add_parser(
        'complete-task',
        help='Complete a task'
    )
    complete_parser.add_argument(
        'user',
        help='Name of the user'
    )
    complete_parser.add_argument(
        'title',
        help='Title of the task'
    )
    complete_parser.set_defaults(func=complete_task)
    
    # Parse arguments and execute the appropriate function
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()