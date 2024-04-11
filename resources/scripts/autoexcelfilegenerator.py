import os
import xlwt
import math

def find_closest_number(file_path, target):
    # Initialize variables to store the closest number and its corresponding value
    closest_number = None
    corresponding_value = None

    # Read the .dat file
    with open(file_path, 'r') as file:
        lines = file.readlines()[3:]  # Skip the first three lines
        for line in lines:
            # Split the line by whitespace
            parts = line.split()
            # Extract the first number from each line
            number = float(parts[0])
            if closest_number is None or (abs(target - number) < abs(target - closest_number)):
                closest_number = number
                corresponding_value = float(parts[1])

    # Return the closest number and its corresponding value
    return closest_number, corresponding_value


def convert_to_degrees(radians):
    return round(math.degrees(radians))  # Round to the nearest integer


def extract_description_line(file_path):
    description_line = None
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip().startswith("Description:"):
                description_line = next(file).strip()
                break
    return description_line


def extract_tire_info(file_path):
    tire_info = []
    with open(file_path, 'r', encoding='utf-8') as file:
        found_tire_section = False
        for line in file:
            if line.strip() == "## Tires #################################################################":
                found_tire_section = True
                continue
            elif line.strip() == "## Brake #################################################################":
                break
            elif found_tire_section and line.strip().startswith("Tire."):
                tire_info.append(line.strip().split('=')[1].strip())
    return tire_info


def format_description(description):
    return '_'.join(description.split())


def create_excel_file(description, tire_info, corresponding_values, excel_folder_path):
    excel_file_path = os.path.join(excel_folder_path, f"{description}.xls")
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Sheet1')
    # Add headings in bold
    bold_style = xlwt.easyxf('font: bold on')
    headings = ["Vehicle Name", "Tire", "ay_4", "ay_6", "ay_8"]
    for col, heading in enumerate(headings):
        worksheet.write(0, col, heading, bold_style)
    # Write description to cell A2
    worksheet.write(1, 0, description)
    # Write tire info to respective cells
    for row, tire in enumerate(tire_info):
        worksheet.write(row + 1, 1, tire)
    # Write corresponding values to respective cells
    worksheet.write(1, 2, convert_to_degrees(corresponding_values[0]))  # ay_4
    worksheet.write(1, 3, convert_to_degrees(corresponding_values[1]))  # ay_6
    worksheet.write(1, 4, convert_to_degrees(corresponding_values[2]))  # ay_8
    workbook.save(excel_file_path)
    print(f"Excel file '{excel_file_path}' created successfully!")


def main():
    vff_folder_path = os.environ.get('VFF_FOLDER_PATH')
    dat_folder_path = os.environ.get('DAT_FOLDER_PATH')  # Adjust this path
    excel_folder_path = os.environ.get('EXCEL_FOLDER_PATH')

    # Create excel_folder_path if it does not exist
    if not os.path.exists(excel_folder_path):
        os.makedirs(excel_folder_path)
    
    for vff_filename in os.listdir(vff_folder_path):
        if vff_filename.endswith("_VFF"):
            vff_file_path = os.path.join(vff_folder_path, vff_filename)
            description_line = extract_description_line(vff_file_path)
            tire_info = extract_tire_info(vff_file_path)

            if description_line:
                formatted_description = format_description(description_line)
                dat_filename = formatted_description + ".dat"
                dat_file_path = os.path.join(dat_folder_path, dat_filename)
                closest_number_4, corresponding_value_4 = find_closest_number(dat_file_path, 4)
                closest_number_6, corresponding_value_6 = find_closest_number(dat_file_path, 6)
                closest_number_8, corresponding_value_8 = find_closest_number(dat_file_path, 8)

                corresponding_values = [corresponding_value_4, corresponding_value_6, corresponding_value_8]
                create_excel_file(formatted_description, tire_info, corresponding_values, excel_folder_path)
            else:
                print(f"Description line not found in the file '{vff_file_path}'.")


if __name__ == "__main__":
    main()
