#!/usr/bin/env python3
"""
Task Manager CLI Tool

A command-line interface for managing tasks associated with users.
"""

import argparse
from lib.models import Task, User


# Global data store for the CLI session
users = {}


def add_task(args):
    """
    Add a new task for a user.
    
    Args:
        args: Command-line arguments containing user and title
    """
    user = users.get(args.user) or User(args.user)
    users[args.user] = user
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
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers()

    add_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_parser.add_argument("user")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=add_task)

    complete_parser = subparsers.add_parser("complete-task", help="Complete a task")
    complete_parser.add_argument("user")
    complete_parser.add_argument("title")
    complete_parser.set_defaults(func=complete_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()