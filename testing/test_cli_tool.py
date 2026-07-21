#!/usr/bin/env python3
"""
Test runner for the CLI tool.
This script simulates the test suite that will be used for grading.
"""

import subprocess
import sys


def run_command(cmd):
    """Run a CLI command and return the output."""
    result = subprocess.run(
        f"python cli_tool.py {cmd}",
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr, result.returncode


def test_add_task():
    """Test the add-task command."""
    print("Testing: Adding Task for User")
    
    # Test 1: Add a new task for a new user
    stdout, stderr, code = run_command('add-task Alice "Write unit tests"')
    if "📌 Task 'Write unit tests' added to Alice." in stdout:
        print("  ✅ Test 1 passed: Task added successfully")
    else:
        print(f"  ❌ Test 1 failed: Expected task added message, got: {stdout}")
        return False
    
    # Test 2: Add another task for the same user
    stdout, stderr, code = run_command('add-task Alice "Build CLI tool"')
    if "📌 Task 'Build CLI tool' added to Alice." in stdout:
        print("  ✅ Test 2 passed: Second task added successfully")
    else:
        print(f"  ❌ Test 2 failed: Expected task added message, got: {stdout}")
        return False
    
    return True


def test_complete_task():
    """Test the complete-task command."""
    print("\nTesting: Completing a Task for User")
    
    # First, add a task
    run_command('add-task Bob "Test completion"')
    
    # Complete the task
    stdout, stderr, code = run_command('complete-task Bob "Test completion"')
    if "✅ Task 'Test completion' completed." in stdout:
        print("  ✅ Test passed: Task completed successfully")
        return True
    else:
        print(f"  ❌ Test failed: Expected completion message, got: {stdout}")
        return False


def test_task_class():
    """Test the Task class logic."""
    print("\nTesting: Task Class Logic")
    
    from models import Task
    
    # Create a task
    task = Task("Test task")
    if not task.completed:
        print("  ✅ Test 1 passed: Task created with completed=False")
    else:
        print("  ❌ Test 1 failed: Task should start as incomplete")
        return False
    
    # Complete the task
    task.complete()
    if task.completed:
        print("  ✅ Test 2 passed: Task marked as completed")
    else:
        print("  ❌ Test 2 failed: Task should be completed")
        return False
    
    return True


def test_user_class():
    """Test the User class logic."""
    print("\nTesting: User Class Logic")
    
    from models import Task, User
    
    # Create a user
    user = User("Charlie")
    if user.name == "Charlie":
        print("  ✅ Test 1 passed: User created with correct name")
    else:
        print("  ❌ Test 1 failed: User name not set correctly")
        return False
    
    # Add a task
    task = Task("User test task")
    user.add_task(task)
    if len(user.tasks) == 1:
        print("  ✅ Test 2 passed: Task added to user")
    else:
        print("  ❌ Test 2 failed: Task not added correctly")
        return False
    
    return True


def test_completion_message():
    """Test that the completion message is correctly printed."""
    print("\nTesting: Task Completion Message")
    
    from models import Task
    import io
    import sys
    
    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    # Complete a task
    task = Task("Message test")
    task.complete()
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Check the output
    if "✅ Task 'Message test' completed." in captured_output.getvalue():
        print("  ✅ Test passed: Correct completion message printed")
        return True
    else:
        print(f"  ❌ Test failed: Expected completion message, got: {captured_output.getvalue()}")
        return False


def test_cli_state():
    """Test that the CLI maintains correct state."""
    print("\nTesting: CLI Maintains Correct State")
    
    # Add a task and complete it in separate commands
    run_command('add-task David "State test"')
    stdout, stderr, code = run_command('complete-task David "State test"')
    
    if "✅ Task 'State test' completed." in stdout:
        print("  ✅ Test passed: CLI maintains state between commands")
        return True
    else:
        print(f"  ❌ Test failed: State not maintained, got: {stdout}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("RUNNING TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_add_task,
        test_complete_task,
        test_task_class,
        test_user_class,
        test_completion_message,
        test_cli_state
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED! Ready for submission.")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please review the code.")
        return 1


if __name__ == "__main__":
    sys.exit(main())