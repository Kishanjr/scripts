import pandas as pd

def filter_alphanumeric_rows(input_file, name_column='name',
                             cleaned_file='filtered_data.csv',
                             removed_file='non_alphanumeric.csv'):
    """
    Filters rows where the specified 'name_column' is alphanumeric (contains both letters and numbers).
    Saves:
        - Cleaned data (alphanumeric rows only) to 'cleaned_file'
        - Removed rows (non-alphanumeric) to 'removed_file'
    """

    # Read the CSV
    data = pd.read_csv(input_file)

    # Lists to collect indices and rows to remove
    non_alpha_indices = []
    non_alpha_rows = []

    # Iterate through rows
    for index, row in data.iterrows():
        val = str(row[name_column])
        if any(c.isalpha() for c in val) and any(c.isdigit() for c in val):
            # Alphanumeric, keep it
            continue
        else:
            # Not alphanumeric, mark for removal
            non_alpha_indices.append(index)
            non_alpha_rows.append(row)

    # DataFrame of removed rows
    non_alpha_df = pd.DataFrame(non_alpha_rows)

    # Drop non-alphanumeric rows from original data
    data_cleaned = data.drop(index=non_alpha_indices)

    # Save files
    non_alpha_df.to_csv(removed_file, index=False)
    data_cleaned.to_csv(cleaned_file, index=False)

    print(f"Saved cleaned data to: {cleaned_file}")
    print(f"Saved removed (non-alphanumeric) rows to: {removed_file}")
