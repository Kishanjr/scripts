import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from fuzzywuzzy import fuzz

# Load the Excel file
file_path = "your_excel_file.xlsx"
sheet_with_names = "Sheet1"  # Replace with the sheet containing the list of names

# Read the sheet with names into a pandas DataFrame
names_df = pd.read_excel(file_path, sheet_name=sheet_with_names)

# Normalize names for comparison in "First Name Last Name" format
list_of_names = names_df['Name'].str.strip().str.lower().tolist()

# Load the workbook
wb = load_workbook(file_path)

# Define the highlight style
highlight_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Yellow fill

# Helper function to transform "Last Name, First Name" to "First Name Last Name"
def transform_name_format(name):
    if "," in name:
        last, first = name.split(",", 1)
        return f"{first.strip()} {last.strip()}"
    return name.strip()

# Define a function to check for a match using fuzzy matching
def is_match(cell_value, name_list, threshold=75):
    transformed_value = transform_name_format(cell_value.lower())  # Transform the format
    for name in name_list:
        # Calculate the similarity ratio
        if fuzz.partial_ratio(transformed_value, name) >= threshold:
            return True
    return False

# Process all sheets except the one containing the names
for sheet_name in wb.sheetnames:
    if sheet_name == sheet_with_names:
        continue  # Skip the sheet with the names list

    ws = wb[sheet_name]
    print(f"Processing sheet: {sheet_name}")

    # Check each cell in the third column (C) and highlight matches
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=3, max_col=3):  # Adjust column range as needed
        for cell in row:
            if cell.value:
                cell_value = str(cell.value).strip()
                if is_match(cell_value, list_of_names):
                    cell.fill = highlight_fill

# Save the updated file
wb.save("updated_excel_file_with_matches.xlsx")
print("Pattern matching and highlighting complete! File saved as 'updated_excel_file_with_matches.xlsx'.")
