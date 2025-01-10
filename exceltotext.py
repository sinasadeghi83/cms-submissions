import os
import pandas as pd

def convert_excel_to_text(root_folder):
    """
    Convert all Excel files in subfolders of root_folder to text files.

    Args:
        root_folder (str): Path to the root folder containing subfolders with Excel files.
    """
    # Loop through all folders and subfolders
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            # Check if the file is an Excel file
            if filename.endswith(('.xlsx', '.xls')):
                # Construct full file path
                excel_path = os.path.join(foldername, filename)

                # Read the Excel file
                try:
                    df = pd.read_excel(excel_path)

                    # Check if required columns are present
                    required_columns = ["User", "Task", "Score", "Time", "FileID"]
                    if not all(column in df.columns for column in required_columns):
                        print(f"Skipping file {filename}: Missing required columns.")
                        continue

                    # Construct the text file path
                    text_filename = os.path.splitext(filename)[0] + ".txt"
                    text_path = os.path.join(foldername, text_filename)

                    # Write the DataFrame to a text file
                    df.to_csv(text_path, sep='\t', index=False, header=True)
                    print(f"Converted {filename} to {text_filename}")
                except Exception as e:
                    print(f"Failed to process file {filename}: {e}")

if __name__ == "__main__":
    # Specify the root folder
    root_folder = input("Enter the path to the root folder: ")

    # Convert Excel files to text files
    convert_excel_to_text(root_folder)
