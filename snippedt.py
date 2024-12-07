df = pd.DataFrame(data)

        # Check if the file exists
        try:
            # If the file exists, append data
            with pd.ExcelWriter(file_path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                start_row = writer.sheets["Sheet1"].max_row
                df.to_excel(writer, index=False, header=False, startrow=start_row)
        except FileNotFoundError:
            # If the file does not exist, create it and write data
            df.to_excel(file_path, index=False)

        print(f"Iteration {iteration}: Data written to Excel.")

# Run the script
if __name__ == "__main__":
    main()
