import os
import time
import psutil
import subprocess
import shutil
import re

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

def replace_TS_MC_file(file_path, replacements):
    """
    Replace text in a file based on a dictionary of replacements.

    Args:
        file_path (str): Path to the file to modify.
        replacements (dict): Dictionary containing old_string -> new_string mappings.

    Returns:
        bool: True if replacements were made successfully, False otherwise.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        modified = False
        with open(file_path, 'w') as file:
            for line in lines:
                for old_string, new_string in replacements.items():
                    if old_string in line:
                        modified_line = line.replace(old_string, new_string)
                        file.write(modified_line)
                        modified = True
                        break
                else:
                    file.write(line)

        if modified:
            print(f"Replacements made in '{file_path}'")
            return True
        else:
            print(f"No replacements made in '{file_path}'")
            return False

    except Exception as e:
        print(f"Error occurred while processing '{file_path}': {e}")
        return False

def run_batch_script(script_path):
    """
    Execute a batch script.

    Args:
        script_path (str): Path to the batch script.

    Raises:
        subprocess.CalledProcessError: If the subprocess call returns a non-zero exit code.
    """
    try:
        process = subprocess.Popen(script_path, shell=True)
        print("Batch script executing....")
        while process.poll() is None:
            time.sleep(5)  # Sleep for 5 seconds
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def copy_and_rename_folder(source_path, destination_path, new_folder_name):

    try:
        source_folder = os.path.join(source_path, 'ModelCheck')

        if not os.path.exists(source_folder):
            print(f"Error: Source folder '{source_folder}' not found.")
            return False

        destination_folder = os.path.join(destination_path, new_folder_name)

        if os.path.exists(destination_folder):
            print(f"Error: Destination folder '{destination_folder}' already exists.")
            return False

        try:
            shutil.copytree(source_folder, destination_folder)
            print(f"Folder '{source_folder}' copied and renamed to '{destination_folder}'")
            return True
        except Exception as copy_error:
            print(f"Error occurred during folder copy: {copy_error}")
            return False

    except Exception as e:
        print(f"Error occurred while preparing folder copy: {e}")
        return False

def replace_vhclfname_in_batch_script(batch_script_path, new_vhclfname):
    """
    Replace the value of VHCLNAME in a batch script.

    Args:
        batch_script_path (str): Path to the batch script.
        new_vhclfname (str): New value for VHCLNAME.

    """
    try:
        with open(batch_script_path, 'r') as file:
            batch_script_content = file.readlines()

        for i, line in enumerate(batch_script_content):
            match = re.match(r'^(\s*SET\s+VHCLNAME\s*=\s*)\s*(.*?)\s*$', line)
            if match:
                batch_script_content[i] = f"{match.group(1)}{new_vhclfname}\n"
                break

        with open(batch_script_path, 'w') as file:
            file.writelines(batch_script_content)

        print(f"Value of VHCLNAME replaced with '{new_vhclfname}' in the batch script.")
    except FileNotFoundError:
        print(f"Error: Batch script '{batch_script_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_folder(folder_path):

    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents deleted.")
    except Exception as e:
        print(f"Error occurred while deleting folder '{folder_path}': {e}")

if __name__ == "__main__":
    batch_script_path = "C:/CM_Test/Frg-Bedatung_Cayenne_E4_CM12/carmaker.bat"
    source_path = "C:/CM_Test/Frg-Bedatung_Cayenne_E4_CM12/SimOutput/ENGPMAKNB022"
    modelcheck_path = "C:/CM_Test/Frg-Bedatung_Cayenne_E4_CM12/ModelCheck"
    vehicle_folder_path = "C:/CM_Test/Frg-Bedatung_Cayenne_E4_CM12/Data/Vehicle"

    replacements = {
        'SIM_MC=0': 'SIM_MC=1',
        'SIM_TS=1': 'SIM_TS=0'
    }

    replace_TS_MC_file(batch_script_path, replacements)

    vhcl_files = [filename for filename in os.listdir(vehicle_folder_path) if filename.endswith("_VFF")]

    for vhcl_file in vhcl_files:
        vhcl_file_path = os.path.join(vehicle_folder_path, vhcl_file)

        wait_until_process_terminated("HIL.exe")
        print("CM is no longer running.")

        replace_vhclfname_in_batch_script(batch_script_path, vhcl_file)

        run_batch_script(batch_script_path)

        wait_until_process_terminated("HIL.exe")
        print("CM is Terminated Successfully.")

        new_folder_name = f"ModelCheck_{vhcl_file[:-4]}"  # Strip '_VFF' from file name

        copied_folder_path = copy_and_rename_folder(source_path, modelcheck_path, new_folder_name)
        if copied_folder_path:
            delete_folder(os.path.join(source_path, 'ModelCheck'))

