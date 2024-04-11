import os
import shutil
import subprocess
from datetime import datetime
import time


def replace_vehicle_value(template_folder_path, new_vehicle_values):
    time.sleep(6)  # Wait for 6 seconds
    with open(template_folder_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(template_folder_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.startswith("Vehicle ="):
                line = f"Vehicle = {new_vehicle_values}\n"
            file.write(line)


def ascii_format_setup(file_path, new_line):
    # Define the line prefix to be modified
    line_startswith = 'DStore.Format'

    # Read the existing content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find and replace the specific line
    for i, line in enumerate(lines):
        if line.startswith(line_startswith):
            lines[i] = new_line
            break  # Stop searching after the line is found and updated

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    print(f'File "{file_path}" has been updated.')

def load_and_start_test_run(test_run_path):
    time.sleep(6)  # Wait for 6 seconds
    carmaker_tm_executable = "C:\\IPG\\carmaker\\win64-12.0.2\\bin\\CM.exe"

    # Command to load test run into CarMaker and start it
    command = [
        carmaker_tm_executable,
        "-run", test_run_path,
        "-start"
    ]

    try:
        # Execute the command
        subprocess.run(command, check=True)
        print("Test run loaded and started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def construct_template_filename(template_folder_path):
    time.sleep(6)  # Wait for 6 seconds
    # Replace special characters in the template path
    modified_path_format = template_folder_path.replace(":", "").replace("\\", "_")
    return modified_path_format


def rename_files(folder_path, template_filename, new_vehicle_value):
    time.sleep(6)  # Wait for 6 seconds
    # Obtain today's date dynamically
    today_date = datetime.now().strftime("%Y%m%d")

    # Construct the search path
    search_path = os.path.join(folder_path, today_date)

    # Loop through files in the search path
    for filename in os.listdir(search_path):
        if filename.startswith(template_filename):
            old_path = os.path.join(search_path, filename)
            if filename.endswith(".dat"):
                # Get the single value from new_vehicle_value
                new_vehicle_value_single = new_vehicle_value.split(",")[0].strip()
                new_filename = f"{new_vehicle_value_single}.dat"
            elif filename.endswith(".dat.info"):
                # Similar process for .info files
                new_vehicle_value_single = new_vehicle_value.split(",")[0].strip()
                new_filename = f"{new_vehicle_value_single}_info.txt"
            new_path = os.path.join(search_path, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed '{filename}' to '{os.path.basename(new_path)}'.")

def copy_files_to_log_folder(src_folder, dest_folder):
    time.sleep(6)  # Wait for 6 seconds
    # Obtain today's date dynamically
    today_date = datetime.now().strftime("%Y%m%d")
    src_path = os.path.join(src_folder, today_date)

    # Copy files to the log folder
    for file in os.listdir(src_path):
        src_file_path = os.path.join(src_path, file)
        dest_file_path = os.path.join(dest_folder, file)
        shutil.copy(src_file_path, dest_file_path)
        print(f"Copied '{file}' to '{dest_folder}'.")

    # Delete files from the source folder
    for file in os.listdir(src_path):
        file_path = os.path.join(src_path, file)
        os.remove(file_path)
        print(f"Deleted '{file}' from '{src_path}'.")


def main():
    # Paths
    template_folder_path = os.environ.get('TEMPLATE_FOLDER_PATH')
    vehicle_folder_path = os.environ.get('VEHICLE_FOLDER_PATH')
    output_folder = os.environ.get('OUTPUT_FOLDER')
    log_folder = os.environ.get('LOG_FOLDER')
    format_file_config_path = os.environ.get('FORMAT_FILE_CONFIG_PATH')

    ascii_format = 'DStore.Format = ascii\n'

    # Initial settings for ascii format file generation
    ascii_format_setup(format_file_config_path, ascii_format)
    
    # Get list of filenames in the vehicle folder
    for filename in os.listdir(vehicle_folder_path):
        new_vehicle_value = filename  # Use the filename as the new vehicle value

        # Replace vehicle values in the template file
        replace_vehicle_value(template_folder_path, new_vehicle_value)
        print("Vehicle values replaced successfully.")

        # Load and start the test series
        load_and_start_test_run(template_folder_path)

        # Construct the modified template file path
        modified_template_path = construct_template_filename(template_folder_path)

        # Rename .dat file
        rename_files(output_folder, modified_template_path, new_vehicle_value)

        # Copy renamed files to the log folder and delete from the source folder
        copy_files_to_log_folder(output_folder, log_folder)


if __name__ == "__main__":
    main()
