import psutil
import time

def is_process_running(process_name):
    """Check if a process with the given name is currently running."""
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False

def wait_until_process_terminated(process_name):
    """Wait until a process with the given name is terminated."""
    while is_process_running(process_name):
        time.sleep(5)  # Check every 5 seconds

    print(f"{process_name} is no longer running.")
