import requests
import re
import threading
import time

def extract_domain(url):
    # Define a regex pattern to match the domain in a URL
    pattern = re.compile(r'https?://([^/?]+)')
    
    # Use the pattern to search for the domain in the URL
    match = pattern.search(url)
    
    # If a match is found, return the domain group
    if match:
        return match.group(1)
    
    # If no match is found, return None
    return None

def similarity_percentage(str1, str2):
    # Convert strings to sets of characters
    set1 = set(str1)
    set2 = set(str2)

    # Calculate the intersection and union of characters
    intersection = set1.intersection(set2)
    union = set1.union(set2)

    # Calculate the percentage of similarity
    percentage = len(intersection) / len(union) * 100

    return percentage

def compare_strings(str1, str2, threshold=40):
    # Check if the similarity percentage exceeds the threshold
    return similarity_percentage(str1, str2) >= threshold

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
def is_url_taken(url):
    try:
        response = requests.get(url, headers=headers, verify=True)
        # Check if the response status code indicates success (e.g., 2xx)
        return response.status_code // 100 == 2
    except requests.RequestException:
        # An exception occurred, indicating that the URL is not reachable
        return False

def clean_and_lower(input_string):
    # Remove spacing and convert to lowercase
    cleaned_string = input_string.replace(" ", "").lower()
    return cleaned_string


class TaskExecutionTimeout(Exception):
    pass

def execute_task_with_timeout(task_function, timeout=6):
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