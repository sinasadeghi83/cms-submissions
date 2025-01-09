import os
from openpyxl import Workbook

# Base URL
base_url = "http://exam.ce.aut.ac.ir/aws/submission_file/"

# Function to download the file
def download_file(client, file_id, user_folder, filename=None):
    if filename == None:
        filename = f"{file_id}.c"
    url = f"{base_url}{file_id}"
    response = client.get(url)
    
    if response.status_code == 200:
        file_path = os.path.join(user_folder, filename)  # Change the file extension as needed
        with open(file_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download file {file_id} from {url}.")

def store_excel(entries, user_folder):
    path = f"{user_folder}/stats{entries[0]["User"]}.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    header = ("User", "Task", "Score", "Time", "FileID")
    sheet.append(header)
    with open(f"{user_folder}/text_stats.txt", 'wb') as f:
        for entry in entries:
            sheet.append(list(entry.values()))
            f.write(f"\n\n{string_line()}\nFileID:{entry['fileID']}\nTask:{entry["Task"]}\nScore:{entry["Score"]}\nTime:{entry["Time"]}\n{string_line()}\n")
    workbook.save(filename=path)

def string_line():
    myline = ""
    for i in range(20):
        myline += "-"
    return myline
        


