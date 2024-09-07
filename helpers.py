import httpx as requests
import traceback

def get_latest_browser_useragent():
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

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
