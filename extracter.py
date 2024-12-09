import re
from bs4 import BeautifulSoup

def extract_score(input_string):
    match = re.search(r'\(([\d.]+) / [\d.]+\)', input_string)
    if match:
        return float(match.group(1))  # Convert the extracted score to float
    return None  # Return None if no match is found

def extract_page_data(page_data):
    soup = BeautifulSoup(page_data, "lxml")

    # Extract all page links
    pages_div = soup.find("div", {"id":"submissions"}).find_next("div")

    pages_links = []
    if pages_div:
        pages_links = [a['href'] for a in pages_div.find_all('a', href=True)]

    # Extract (Time, User, Task, fileID) as dictionaries
    submissions_table = soup.find("table", class_="bordered")
    data_dict = {}
    if submissions_table:
        rows = submissions_table.find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 3:  # Ensure there's enough data
                time_link = cols[0].find("a", href=True)
                user_link = cols[1].find("a", href=True)
                task_link = cols[2].find("a", href=True)
                status_text = cols[3].get_text(strip=True)
                
                if time_link and user_link and task_link:
                    file_id = time_link['href'].split('/')[-1]
                    data = {
                        "User": user_link.text.strip(),
                        "Task": task_link.text.strip(),
                        "Score": extract_score(status_text),
                        "Time": time_link.text.strip(),
                        "fileID": file_id,
                    }
                    if data["User"] not in data_dict:
                        data_dict[data["User"]] = []
                    data_dict[data["User"]].append(data)

    return data_dict, pages_links
