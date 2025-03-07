import pandas as pd
import os

def csvs_to_excel(csv_folder, output_file):
    # List only files in the folder that end with .csv (case insensitive)
    csv_files = [
        f for f in os.listdir(csv_folder)
        if f.lower().endswith('.csv') and os.path.isfile(os.path.join(csv_folder, f))
    ]
    
    if not csv_files:
        print("No CSV files found in the folder.")
        return

    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for csv_file in csv_files:
            file_path = os.path.join(csv_folder, csv_file)
            # Use file name without extension as sheet name (max 31 characters for Excel)
            sheet_name = os.path.splitext(csv_file)[0][:31]
            try:
                df = pd.read_csv(file_path)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"Converted {csv_file} to sheet '{sheet_name}'")
            except Exception as e:
                print(f"Failed to convert {csv_file}: {e}")

if __name__ == "__main__":
    # Specify the folder containing your CSV files (use '.' for current directory)
    folder = "."
    # Name of the output Excel workbook
    output = "combined.xlsx"
    csvs_to_excel(folder, output)
