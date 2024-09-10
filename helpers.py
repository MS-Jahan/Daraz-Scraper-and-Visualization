import httpx as requests
import traceback
import json
import time, random
import http.server
import socketserver
import webbrowser
import threading
import os

def get_latest_browser_useragent():
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

def serve_report(report_filename):
    port = 8080
    os.chdir('output')  # Change to the output directory
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving report at http://localhost:{port}/{os.path.basename(report_filename)}")
        print(f"Press Ctrl+C to stop the server")
        httpd.serve_forever()

def get_product_details(product_json):
    product = {}
    product["name"] = product_json["name"].strip()
    product["image"] = product_json["image"].strip() if "image" in product_json else None
    product["item_id"] = product_json["itemId"]
    product["discount_percentage"] = float(product_json["discount"].replace("% Off", "")) if "discount" in product_json else 0
    product["rating"] = float(product_json["ratingScore"]) if "ratingScore" in product_json and product_json["ratingScore"].strip() else 0
    product["number_of_reviews"] = float(product_json["review"]) if "review" in product_json and product_json["review"].strip() else 0
    product["location"] = product_json["location"].strip() if "location" in product_json else None
    product["current_price"] = float(product_json["price"])
    product["original_price"] = float(product_json["originalPrice"]) if "originalPrice" in product_json else float(product_json["price"])
    product["url"] = product_json["itemUrl"][2:] if product_json["itemUrl"].startswith("//") else product_json["itemUrl"]
    
    return product

def get_current_page_items(data):
    current_page_products = data["mods"]["listItems"]
    processed_products_obj_arr = []

    for product in current_page_products:
        processed_products_obj_arr.append(get_product_details(product))

    return processed_products_obj_arr

def send_get_request_and_return_json(page, url):
    max_tries = 3
    while max_tries > 0:
        try:
            # page.get(url)
            json_data = page.run_js_loaded('''
                return fetch("''' + url + '''", {
                "method": "GET",
                "mode": "cors",
                "credentials": "include"
                }).then(response => response.json())
                .then(data => {
                    return JSON.stringify(data);
                })
                .catch(err => {
                    return JSON.stringify({error: err.message});
                });
            ''')
            # convert the json string to a python dictionary
            return json.loads(json_data)
            break
        except:
            print("Failed to get data")
            print(traceback.format_exc())
            max_tries -= 1
            random_sleep_time = random.randint(3, 5)
            print(f"Retrying in {random_sleep_time} seconds...")
            time.sleep(random_sleep_time)
        



