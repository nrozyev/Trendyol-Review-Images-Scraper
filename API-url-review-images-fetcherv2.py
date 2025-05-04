import requests
import json
import time
import xml.etree.ElementTree as ET
import re
import os


# Base API endpoint
BASE_URL = "https://apigw.trendyol.com/discovery-mweb-socialgw-service/api/product-review/reviews/{product_id}"
OUTPUT_FILE = "review_media_urls.json"
PAGE_SIZE = 30


def fetch_media_urls(product_id, product_full_url):
    media_urls = []
    page = 0
    total_pages = 3  # Dummy initial value
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    while page < total_pages:
        url = f"{BASE_URL}?page={page}&size={PAGE_SIZE}&storefrontId=1&orderByDirection=DESC&orderByField=Score&channelId=1"
        response = requests.get(url.format(product_id=product_id), headers = headers)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}, status code: {response.status_code}")
            break

        data = response.json()
        #print(data)
        reviews = data.get("reviews", {}).get("content", [])
        
        total_pages = data.get("reviews", {}).get("totalPages", total_pages)
        print(total_pages)

        for review in reviews:
            for media in review.get("mediaFiles", []):
                media_urls.append(media.get("url"))

        print(f"Fetched page {page + 1}/{total_pages}")
        page += 1
        time.sleep(3)  # Sleep to avoid rate-limiting

    return {"Product": f'{product_full_url}', "image_urls": media_urls}

def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def iter_product_ids(urls):
    for product_url in urls:
            match = re.search(r'-p-(\d+)', product_url)
            if match:
                yield (match.group(1), product_url)

if __name__ == "__main__":
    # Check if file exists, if not, create it
    json_file_path = "review_media_urls.json"
    json_list = []

    if not os.path.exists(json_file_path):
        with open(json_file_path, "w", encoding="utf-8") as f:
            pass 

    with open("product_urls.json", "r", encoding="utf-8") as f:
        categories = json.load(f)
    
    for category in categories.keys():
        product_urls = categories[category]

        try:     
            for product_id, product_url in iter_product_ids(product_urls):
                full_product_url ="https://www.trendyol.com"+product_url
                object_ = fetch_media_urls(product_id, full_product_url)
                json_list.append(object_)
                print(f"Added {len(object_)} media URLs to jsonl_list")
                save_to_json(json_list, OUTPUT_FILE)
        except(Exception, KeyboardInterrupt):
            save_to_json(json_list, OUTPUT_FILE)
    
        
