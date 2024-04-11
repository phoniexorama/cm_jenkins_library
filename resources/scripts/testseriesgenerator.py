import os
import pandas as pd
import shutil

# Function to replace values in template.ts file
def replace_value(search_string, new_value, template_content):
    index = template_content.find(search_string)
    if index != -1:
        print(f"String '{search_string}' found in template.ts file.")
        lines = template_content.split("\n")
        for i, line in enumerate(lines):
            if search_string in line:
                parts = line.split("=")
                if len(parts) > 1:
                    parts[1] = f' {new_value}'
                    lines[i] = "=".join(parts)
                break
        template_content = "\n".join(lines)
        print(f"Modified content for '{search_string}'.")
    else:
        print(f"String '{search_string}' not found in template.ts file.")
    return template_content

# Function to copy template.ts file to Testseries folder and rename it
def copy_template_to_testseries(template_file_path, destination_folder, new_file_name):
    try:
        # Copy template.ts to Testseries folder
        shutil.copy(template_file_path, destination_folder)
        print(f"Template.ts copied to {destination_folder}")

        # Rename the copied file
        new_file_path = os.path.join(destination_folder, new_file_name)
        os.rename(os.path.join(destination_folder, "template.ts"), new_file_path)
        print(f"Renamed copied file to {new_file_name}")
        return new_file_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Directory containing Excel files
excel_folder = os.environ.get('EXCEL_FOLDER_PATH')

# Read the template.ts file
template_file_path = os.environ.get('TEMPLATE_FILE')
with open(template_file_path, "r") as file:
    template_content = file.read()
print("Read template.ts file content successfully.")

# Iterate over each Excel file in the directory
for file_name in os.listdir(excel_folder):
    if file_name.endswith(".xls"):
        file_path = os.path.join(excel_folder, file_name)
        print(f"Processing Excel file: {file_path}")

        # Read values from VehicleInfo.xlsx
        vehicle_info = pd.read_excel(file_path)
        B2_value = vehicle_info.iloc[0, 1]
        B3_value = vehicle_info.iloc[1, 1]
        B4_value = vehicle_info.iloc[2, 1]
        B5_value = vehicle_info.iloc[3, 1]
        C2_value = vehicle_info.iloc[0, 2]
        D2_value = vehicle_info.iloc[0, 3]
        E2_value = vehicle_info.iloc[0, 4]
        A2_value = vehicle_info.iloc[0, 0]

        # Replace values in template_content
        template_content = replace_value("Step.1.0.Param.0 = Tire.0 KValue", f"Tire.0 KValue {B2_value}", template_content)
        template_content = replace_value("Step.1.0.Param.1 = Tire.1 KValue", f"Tire.1 KValue {B3_value}", template_content)
        template_content = replace_value("Step.1.0.Param.2 = Tire.2 KValue", f"Tire.2 KValue {B4_value}", template_content)
        template_content = replace_value("Step.1.0.Param.3 = Tire.3 KValue", f"Tire.3 KValue {B5_value}", template_content)
        template_content = replace_value("Step.1.2.Var.0.Param", str(int(C2_value)), template_content)
        template_content = replace_value("Step.1.2.Var.1.Param", str(int(D2_value)), template_content)
        template_content = replace_value("Step.1.2.Var.2.Param", str(int(E2_value)), template_content)

        # Define search strings for replacement
        search_strings = ["Step.1.0.Name", "Step.1.0.Vehicle"]

        # Replace values for each search string
        for search_string in search_strings:
            index = template_content.find(search_string)
            if index != -1:
                print(f"String '{search_string}' found in template.ts file.")

                # Find the line containing the search string and replace the value after "="
                lines = template_content.split("\n")
                for i, line in enumerate(lines):
                    if search_string in line:
                        parts = line.split("=")
                        if len(parts) > 1:
                            parts[1] = f' {A2_value}'  # Add a space after "="
                            lines[i] = "=".join(parts)
                        break

                # Join the modified lines and update template_content
                template_content = "\n".join(lines)
                print(f"Modified content for '{search_string}'.")

        # Write the modified content back to the template.ts file
        with open(template_file_path, "w") as file:
            file.write(template_content)
        print("Modified content written back to template.ts file.")

        # Copy template.ts file to Testseries folder and rename it based on A2_value
        destination_folder = os.environ.get('DESTINATION_FOLDER')
        new_file_name = f"{A2_value}.ts"
        copied_file_path = copy_template_to_testseries(template_file_path, destination_folder, new_file_name)
        if copied_file_path:
            print(f"New file created: {copied_file_path}")
        else:
            print("Failed to create new file.")
