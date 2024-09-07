import httpx as requests
import math
import json
import traceback
import time, random
from pprint import pprint

from helpers import *
from database import Database

DB = Database("db.sqlite")
PRINT_ERRORS = True
WAIT_BETWEEN_PAGES = False

def print_error():
    if PRINT_ERRORS:
        print(traceback.format_exc())

category_tag = input("Enter the category tag: ")

URL = f"https://www.daraz.com.bd/{category_tag}/?ajax=true&page=1"

headers = {
    "User-Agent": get_latest_browser_useragent(),
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.5"
}

print("\nFetching 1st page for category:", category_tag)
response = requests.get(URL, headers=headers)

data = []
current_page_items = []
total_items = 0

try:
    data = response.json()
    current_page_items = data["mods"]["listItems"]
    total_items = int(data["mods"]["filter"]["filteredQuatity"])
    number_of_items_in_a_page = int(data["mainInfo"]["pageSize"])
    number_of_pages = math.ceil(total_items / number_of_items_in_a_page)
except:
    print("Failed to get data")
    print_error()
    exit()

print(f"Total items in the category: {total_items}")

# process the first page and save the data to database
DB.batch_insert(get_current_page_items(data))

# iterate over all pages
for page in range(2, number_of_pages + 1):
    print(f"Fetching page {page}...")
    URL = f"https://www.daraz.com.bd/{category_tag}/?ajax=true&page={page}"
    response = requests.get(URL, headers=headers)
    try:
        data = response.json()
        DB.batch_insert(get_current_page_items(data))
    except:
        print(f"Failed to get data for page {page}")
        print_error()
    
    # check if last page
    if page != number_of_pages and WAIT_BETWEEN_PAGES:
        sleep_time = random.randint(3, 5)
        print(f"Waiting for {sleep_time} seconds before fetching the next page...\n")
        time.sleep(sleep_time)

# check how many duplicates are there in the data using item_id
duplicates = DB.check_duplicate_entries_in_db()
print(f"Total duplicate entries: {len(duplicates)}")

if len(duplicates) > 0:
    # pprint(duplicates)
    print("Removing duplicates...")
    DB.remove_duplicates()

print(f"Total items processed: {DB.get_total_items()['COUNT(*)']}")

