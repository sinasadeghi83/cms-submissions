import httpx
import os
from getpass import getpass
from tqdm import tqdm
from extracter import extract_page_data
from store import download_file, store_excel

username = input("Enter admin username: ")
password = getpass("Enter admin password: ")
contestID = input("Enter contest id:")

client = httpx.Client()
r = client.get("http://exam.ce.aut.ac.ir/aws/login?next=%2F")
xsrf = r.cookies["_xsrf"]
r = client.post("http://exam.ce.aut.ac.ir/aws/login", data={"_xsrf":xsrf, "username":username, "password":password})
url = f"http://exam.ce.aut.ac.ir/aws/contest/{contestID}/submissions"
r = client.get(url)

data, page_links = extract_page_data(r.text)

for page_link in tqdm(page_links, desc="Retriving informations from CMS"):
    newUrl = f"{url}/../{page_link}"
    r = client.get(newUrl)
    newData, _ = extract_page_data(r.text)
    for k1, v1 in data.items():
        if k1 in newData:
            data[k1] += newData[k1]
    for k2, v2 in newData.items():
        if k2 not in data:
            data[k2] = v2

# Loop through the list of dictionaries
for user_id, entries in tqdm(data.items(), desc="Downloading submissions"):
    user_folder = f"./submissions/{user_id}"
    
    # Create the directory if it does not exist
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    store_excel(entries, user_folder)
    for entry in entries:
        # Download the file
        download_file(client, entry['fileID'], user_folder)