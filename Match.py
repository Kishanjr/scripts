import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from fuzzywuzzy import fuzz

# Load the Excel file
file_path = "your_excel_file.xlsx"
sheet_with_names = "Sheet1"  # Replace with the actual sheet name
sheet_to_check = "Sheet2"    # Replace with the actual sheet name

# Read the sheets into pandas DataFrames
names_df = pd.read_excel(file_path, sheet_name=sheet_with_names)
check_df = pd.read_excel(file_path, sheet_name=sheet_to_check)

# Assume the column containing names is called "Name"
list_of_names = names_df['Name'].str.lower().tolist()  # Normalize to lowercase for comparison

# Load workbook and sheet for highlighting
wb = load_workbook(file_path)
ws = wb[sheet_to_check]

# Define the highlight style
highlight_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Yellow fill

# Define a function to check for a match using fuzzy matching
def is_match(cell_value, name_list, threshold=80):
    for name in name_list:
        # Calculate the similarity ratio
        if fuzz.partial_ratio(cell_value.lower(), name) >= threshold:
            return True
    return False

# Check each cell in the second sheet and highlight matches
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=1):  # Assuming names are in column A
    for cell in row:
        if cell.value:
            cell_value = str(cell.value).strip()
            if is_match(cell_value, list_of_names):
                cell.fill = highlight_fill

# Save the updated file
wb.save("updated_excel_file_with_matches.xlsx")
print("Pattern matching and highlighting complete! File saved as 'updated_excel_file_with_matches.xlsx'.")
