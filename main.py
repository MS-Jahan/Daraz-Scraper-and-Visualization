from DrissionPage import ChromiumPage, ChromiumOptions
import os
import math
from helpers import *
from config import *
from data_prep import prepare_data
from data_analysis import *
from data_visualization import *
from report_generator import generate_report

# Get the category tag from the URL, example: https://www.daraz.com.bd/toys-action-figures/
PRINT_ERRORS = True
WAIT_BETWEEN_PAGES = True
TRUNCATE_TABLE_BEFORE_INSERT = True
USER_INPUTTED_URL = "https://www.daraz.com.bd/ska-egg-boilers/" # input("Enter the category URL: ")
category_tag = USER_INPUTTED_URL.split("?")[0].rstrip("/").replace("https://www.daraz.com.bd/", "")
URL = f"https://www.daraz.com.bd/{category_tag}/?ajax=true&page="
DB = get_db(TRUNCATE_TABLE_BEFORE_INSERT)

def print_error():
    if PRINT_ERRORS:
        print(traceback.format_exc())

# check the os and set the browser path
if os.name == 'nt':
    browser_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
else:
    browser_path = "/usr/bin/google-chrome-stable"

# with Display(visible=0, size=[1920, 1080]) as display:
op = ChromiumOptions().set_browser_path(browser_path)
# op.headless(True)
op.auto_port()
dp = ChromiumPage(op)
dp.get(USER_INPUTTED_URL)

print("\nFetching 1st page for category:", category_tag)
response = send_get_request_and_return_json(dp, URL+"1")

all_data = []

data = []
current_page_items = []
total_items = 0

# if no logs, data and output directory, create one
if not os.path.exists("logs"):
    os.makedirs("logs")
if not os.path.exists("output"):
    os.makedirs("output")

try:
    data = response
    # save page 1 json data to a file
    with open("logs/page_1.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    current_page_items = data["mods"]["listItems"]
    total_items = int(data["mods"]["filter"]["filteredQuatity"])
    number_of_items_in_a_page = int(data["mainInfo"]["pageSize"])
    number_of_pages = math.ceil(total_items / number_of_items_in_a_page)
except:
    print("Failed to get data")
    print_error()
    # save json data to a file
    with open("logs/failed_page_1.json", "w") as f:
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
            print(f"\nFetching page {page}/{number_of_pages}...")
            response = send_get_request_and_return_json(dp, URL+str(page))
            try:
                data = response
                # save json data to a file
                with open(f"logs/page_{page}.json", "w") as f:
                    f.write(json.dumps(data, indent=4))
                products_in_page = get_current_page_items(data)
                all_data += products_in_page
                print(f"Inserting items from page {page}/{number_of_pages} to the database...")
                proudcts_inputted, total_inserted = DB.batch_insert(products_in_page)
                print(f"Iems processed: {proudcts_inputted}\nItems inserted: {total_inserted}")
            except:
                print(f"Failed to get data for page {page}/{number_of_pages}")
                print_error()
                # save json data to a file
                with open(f"logs/failed_page_{page}.json", "w") as f:
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

# close the browser
dp.close()

# check how many duplicates are there in the data using item_id
duplicates = DB.check_duplicate_entries_in_db()
print(f"Total duplicate entries: {len(duplicates)}")

if len(duplicates) > 0:
    # save duplicates to a file
    with open("logs/duplicates.json", "w") as f:
        f.write(json.dumps(duplicates, indent=4))
    print("Removing duplicates...")
    DB.remove_duplicates()

print(f"Total items processed: {DB.get_total_items()}")

# save all data to a file
with open("logs/all_data.json", "w") as f:
    f.write(json.dumps(all_data, indent=4))

# read the file
with open("logs/all_data.json", "r") as f:
    all_data = json.load(f)

# Data Extraction and Preparation
df = prepare_data(all_data)

# Data Analysis
desc_stats = descriptive_stats(df)
price_stats, price_ranges = price_analysis(df)
avg_discount, max_discount_products = discount_analysis(df)
avg_rating, rating_dist = rating_review_analysis(df)
location_counts = location_analysis(df)
correlations = correlation_analysis(df)

# Data Visualization
price_histogram = plot_histogram(df['current_price'], "Price Distribution", "Price", "Frequency", "output/price_histogram.png")
discount_histogram = plot_histogram(df['discount_percentage'], "Discount Distribution", "Discount (%)", "Frequency", "output/discount_histogram.png")
rating_histogram = plot_histogram(df['rating'], "Rating Distribution", "Rating", "Frequency", "output/rating_histogram.png")

price_discount_scatter = plot_scatter(df['current_price'], df['discount_percentage'], "Price vs. Discount", "Price", "Discount (%)", "output/price_discount_scatter.png")
rating_reviews_scatter = plot_scatter(df['rating'], df['number_of_reviews'], "Rating vs. Reviews", "Rating", "Number of Reviews", "output/rating_reviews_scatter.png")

location_bar_chart = plot_bar_chart(location_counts.index, location_counts.values, "Product Locations", "Location", "Count", "output/location_bar_chart.png")

# Example: Box plot of price distribution by location (you may need to adjust this based on your data)
location_price_boxplot = plot_box_plot([df['current_price'][df['location'] == loc] for loc in location_counts.index],
                                     location_counts.index,
                                     "Price Distribution by Location", "Price", "output/location_price_boxplot.png")
# Report Generation
visualizations = {
    'price_histogram': price_histogram,
    'discount_histogram': discount_histogram,
    'rating_histogram': rating_histogram,
    'price_discount_scatter': price_discount_scatter,
    'rating_reviews_scatter': rating_reviews_scatter,
    'location_bar_chart': location_bar_chart,
    'location_price_boxplot': location_price_boxplot
}
report_filename = generate_report(desc_stats, price_stats, price_ranges, avg_discount,
                                max_discount_products, avg_rating, rating_dist,
                                location_counts, correlations, visualizations)

print(f"Report generated successfully: {report_filename}")
DB.close()

# open the report in the default browser
try:
    os.system(f"start {report_filename}")
except:
    print("Failed to open the report automatically. Please open the report manually.")

server_thread = threading.Thread(target=serve_report, args=(report_filename,))
server_thread.start()

print(f"You can view the report by opening http://localhost:8080/{os.path.basename(report_filename)} in your web browser")

# Keep the main thread running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Shutting down the server...")