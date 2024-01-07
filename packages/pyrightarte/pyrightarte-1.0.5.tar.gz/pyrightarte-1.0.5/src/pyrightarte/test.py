import threading
import time

class TaskExecutionTimeout(Exception):
    pass

def example_task():
    for i in range(1):
        time.sleep(1)  # Simulate work
    return "Task completed successfully"

def execute_task_with_timeout(task_function, timeout=5):
    # Create a flag to indicate if the task should be terminated

    result = None
    # Function to be executed in a separate thread
    def thread_function():
        nonlocal result
        try:
            result = task_function()
            return result
        except TaskExecutionTimeout as e:
            print(f"Task execution timeout: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Create a thread for the task
    task_thread = threading.Thread(target=thread_function)

    # Start the thread
    task_thread.start()

    # Wait for the thread to complete or until the timeout is reached
    elapsed_time = 0
    while task_thread.is_alive() and elapsed_time < timeout:
        time.sleep(1)
        elapsed_time += 1
    

    # Return the result if available
    return result

# Example usage:
print(time.time())
result = execute_task_with_timeout(example_task)
print(time.time())

if result:
    print(f"Task result: {result}")
else:
    print("Task did not complete within 5 seconds.")
