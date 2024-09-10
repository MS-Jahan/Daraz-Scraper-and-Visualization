import httpx as requests
import math
import json
import traceback
import time, random
from pprint import pprint
from helpers import *
from database import Database

DB = Database("localhost", "root", "1234", "products")
session = requests.Client(
    headers = {
    "User-Agent": get_latest_browser_useragent(),
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.5"
    },
    timeout = (10, 10),
    http2=True
)
PRINT_ERRORS = True
WAIT_BETWEEN_PAGES = True

def print_error():
    if PRINT_ERRORS:
        print(traceback.format_exc())

# Get the category tag from the URL, example: https://www.daraz.com.bd/toys-action-figures/
URL = input("Enter the category URL: ")
category_tag = URL.split("?")[0].rstrip("/").replace("https://www.daraz.com.bd/", "")
URL = f"https://www.daraz.com.bd/{category_tag}/?ajax=true&page="



print("\nFetching 1st page for category:", category_tag)
response = session.get(URL+"1")

all_data = []

data = []
current_page_items = []
total_items = 0

try:
    data = response.json()
    # save page 1 json data to a file
    with open("page_1.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    current_page_items = data["mods"]["listItems"]
    total_items = int(data["mods"]["filter"]["filteredQuatity"])
    number_of_items_in_a_page = int(data["mainInfo"]["pageSize"])
    number_of_pages = math.ceil(total_items / number_of_items_in_a_page)
except:
    print("Failed to get data")
    print_error()
    # save json data to a file
    with open("failed_page_1.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    exit()

print(f"Total items in the category: {total_items}")
print(f"Number of pages: {number_of_pages}")

# process the first page and save the data to database
products_in_page = get_current_page_items(data)
all_data += products_in_page
print(f"Inserting items from page 1 to the database...")
proudcts_inputted, total_inserted = DB.batch_insert(products_in_page)
print(f"Iems processed: {proudcts_inputted}\nItems inserted: {total_inserted}")

# iterate over all pages
for page in range(2, number_of_pages + 1):
    max_tries = 3
    while max_tries > 0:
        try:
            print(f"\nFetching page {page}...")
            response = session.get(URL+str(page))
            try:
                data = response.json()
                # save json data to a file
                with open(f"page_{page}.json", "w") as f:
                    f.write(json.dumps(data, indent=4))
                products_in_page = get_current_page_items(data)
                all_data += products_in_page
                print(f"Inserting items from page {page} to the database...")
                proudcts_inputted, total_inserted = DB.batch_insert(products_in_page)
                print(f"Iems processed: {proudcts_inputted}\nItems inserted: {total_inserted}")
            except:
                print(f"Failed to get data for page {page}")
                print_error()
                # save json data to a file
                with open(f"failed_page_{page}.json", "w") as f:
                    f.write(json.dumps(data, indent=4))
            
            # check if last page
            if page != number_of_pages and WAIT_BETWEEN_PAGES:
                sleep_time = random.randint(3, 5)
                print(f"Waiting for {sleep_time} seconds before fetching the next page...")
                time.sleep(sleep_time)
            break
        except:
            print("Failed to get data")
            print_error()
            print("Retrying...")
            max_tries -= 1

# check how many duplicates are there in the data using item_id
duplicates = DB.check_duplicate_entries_in_db()
print(f"Total duplicate entries: {len(duplicates)}")

if len(duplicates) > 0:
    # save duplicates to a file
    with open("duplicates.json", "w") as f:
        f.write(json.dumps(duplicates, indent=4))
    # print("Removing duplicates...")
    # DB.remove_duplicates()

print(f"Total items processed: {DB.get_total_items()}")

# save all data to a file
with open("all_data.json", "w") as f:
    f.write(json.dumps(all_data, indent=4))

DB.close()

