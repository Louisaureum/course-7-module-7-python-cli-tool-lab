#!/usr/bin/env python3
"""
Test suite for the CLI tool.
This matches the autograder requirements.
"""

import subprocess
import sys
import os

# Add lib directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def run_command(cmd):
    """Run a CLI command and return the output."""
    # Use the correct path to cli_tool.py
    cli_path = os.path.join(os.path.dirname(__file__), '..', 'lib', 'cli_tool.py')
    full_cmd = f"python {cli_path} {cmd}"
    result = subprocess.run(
        full_cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr, result.returncode


def test_add_task():
    """Test the add-task command."""
    print("\n📋 Testing: Adding Task for User")
    
    # Test adding a task
    stdout, stderr, code = run_command('add-task Alice "Write unit tests"')
    
    if "📌 Task 'Write unit tests' added to Alice." in stdout:
        print("  ✅ PASSED: Task added successfully")
        return True
    else:
        print(f"  ❌ FAILED: Expected task added message, got: {stdout}")
        return False


def test_complete_task():
    """Test the complete-task command."""
    print("\n📋 Testing: Completing a Task for User")
    
    # First add a task
    run_command('add-task Bob "Test completion"')
    
    # Then complete it
    stdout, stderr, code = run_command('complete-task Bob "Test completion"')
    
    if "✅ Task 'Test completion' completed." in stdout:
        print("  ✅ PASSED: Task completed successfully")
        return True
    else:
        print(f"  ❌ FAILED: Expected completion message, got: {stdout}")
        return False


def test_task_class_logic():
    """Test the Task class logic."""
    print("\n📋 Testing: Task Class Logic")
    
    from lib.models import Task
    
    # Create a task
    task = Task("Test task")
    if not task.completed:
        print("  ✅ PASSED: Task created with completed=False")
    else:
        print("  ❌ FAILED: Task should start as incomplete")
        return False
    
    # Complete the task
    task.complete()
    if task.completed:
        print("  ✅ PASSED: Task marked as completed")
    else:
        print("  ❌ FAILED: Task should be completed after complete()")
        return False
    
    return True


def test_user_class_logic():
    """Test the User class logic."""
    print("\n📋 Testing: User Class Logic")
    
    from lib.models import Task, User
    
    # Create a user
    user = User("Charlie")
    if user.name == "Charlie":
        print("  ✅ PASSED: User created with correct name")
    else:
        print("  ❌ FAILED: User name not set correctly")
        return False
    
    # Add a task
    task = Task("User test task")
    user.add_task(task)
    if len(user.tasks) == 1 and user.tasks[0].title == "User test task":
        print("  ✅ PASSED: Task added to user correctly")
    else:
        print("  ❌ FAILED: Task not added correctly")
        return False
    
    return True


def test_completion_message():
    """Test that the completion message is correctly printed."""
    print("\n📋 Testing: Task Completion Message")
    
    from lib.models import Task
    import io
    
    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    # Complete a task
    task = Task("Message test")
    task.complete()
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Check the output
    expected = "✅ Task 'Message test' completed."
    if expected in captured_output.getvalue():
        print("  ✅ PASSED: Correct completion message printed")
        return True
    else:
        print(f"  ❌ FAILED: Expected '{expected}', got: {captured_output.getvalue()}")
        return False


def test_cli_state():
    """Test that the CLI maintains correct state."""
    print("\n📋 Testing: CLI Maintains Correct State")
    
    # Add a task and complete it in separate commands
    run_command('add-task David "State test"')
    stdout, stderr, code = run_command('complete-task David "State test"')
    
    if "✅ Task 'State test' completed." in stdout:
        print("  ✅ PASSED: CLI maintains state between commands")
        return True
    else:
        print(f"  ❌ FAILED: State not maintained, got: {stdout}")
        return False


def test_error_handling():
    """Test error handling for non-existent users and tasks."""
    print("\n📋 Testing: Error Handling")
    
    # Test with non-existent user
    stdout, stderr, code = run_command('complete-task NonExistent "Some task"')
    if "❌ User not found." in stdout:
        print("  ✅ PASSED: User not found error handled")
    else:
        print(f"  ❌ FAILED: Expected user not found error, got: {stdout}")
        return False
    
    # First add a user with a task
    run_command('add-task Eve "Existing task"')
    
    # Then try to complete a non-existent task
    stdout, stderr, code = run_command('complete-task Eve "Non-existent task"')
    if "❌ Task not found." in stdout:
        print("  ✅ PASSED: Task not found error handled")
    else:
        print(f"  ❌ FAILED: Expected task not found error, got: {stdout}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 RUNNING TEST SUITE FOR CLI TOOL")
    print("=" * 60)
    
    tests = [
        test_add_task,
        test_complete_task,
        test_task_class_logic,
        test_user_class_logic,
        test_completion_message,
        test_cli_state,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Ready for submission.")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please review the code.")
        return 1


if __name__ == "__main__":
    sys.exit(main())