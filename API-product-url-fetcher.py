import requests
import json
import time
import xml.etree.ElementTree as ET
import re
import os
from itertools import islice
import keyboard


def fetch_product_urls(
        CATEGORY,
        CATEGORY_BASE_URL="https://apigw.trendyol.com/discovery-mweb-searchgw-service/api/search-v2/products/",
        PI=0,
        OFFSET="",
        OFFSET_PARAMETERS=""):
                                headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                  "Chrome/120.0.0.0 Safari/537.36"
                                }
                                cat_url = (
                                    f"{CATEGORY_BASE_URL}?pi={PI}"
                                    f"&storeId=&pathModel=%2F{CATEGORY}"
                                    f"&searchStrategy=DEFAULT&language=tr"
                                    f"&storefrontId=1&disableMerchant=true"
                                    f"&offset={OFFSET}&offsetParameters={OFFSET_PARAMETERS}"
                                    f"&channelId=1&culture=tr-TR"
                                )
                                #print(cat_url)
                                response =requests.get(cat_url, headers=headers)
                                try:    
                                    data=response.json()
                                except ValueError:
                                    print(f"Non-JSON response received. Status code: {response.status_code}")
                                    print("Response content:", response.text[:200])
                                    return None, None, None
                                products = data.get("products", [])
                                OFFSET=data.get("offset")
                                OFFSET_PARAMETERS=data.get("offsetParameters")
                                product_urls=[]
                                for product in products:
                                      product_urls.append(product.get("url"))
                                PI=PI+1
                                return (product_urls, OFFSET, OFFSET_PARAMETERS)

def append_to_json_file(filepath, category, product_urls):
    # Step 1: Load existing data if file exists
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Step 2: Append new data
    if isinstance(data, dict) and category not in data:
        data[category] = product_urls        
    elif isinstance(data, dict) and category in data:
        data[category] = data[category] + product_urls
    else:
        raise ValueError("Expected the JSON file to contain a dict.")

    # Step 3: Write back the updated list
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)                

if __name__ == "__main__":
    PI, OFFSET, OFFSET_PARAMETERS = 0, "", ""
    # Check if file exists, if not, create it
    review_image_urls_path = "review_media_urls.json"

    
    #with open("product_urls_by_category.json", "w", encoding="utf-8") as f:
    #    json.dump([], f, ensure_ascii=False, indent=4)

    if not os.path.exists(review_image_urls_path):
        with open(review_image_urls_path, "w", encoding="utf-8") as f:
            pass 

    sitemap_categories_url = 'https://www.trendyol.com/sitemap_categories.xml'
    response = requests.get(sitemap_categories_url)
    root = ET.fromstring(response.content)

    # Namespace dictionary for XML parsing
    namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'image': 'http://www.google.com/schemas/sitemap-image/1.1',
        'xhtml': 'http://www.w3.org/1999/xhtml'}

    # Step 2: Iterate through each sitemap URL
    urls_for_categories = (elem.text for elem in root.findall('ns:url/ns:loc', namespaces))

    for url in urls_for_categories:
        category = os.path.basename(url)
        product_urls, OFFSET, OFFSET_PARAMETERS = fetch_product_urls(category)
        append_to_json_file("product_urls.json", category, product_urls)
        
        
        while True:
            
            product_urls, OFFSET, OFFSET_PARAMETERS = fetch_product_urls(category, PI=PI, OFFSET=OFFSET, OFFSET_PARAMETERS=OFFSET_PARAMETERS)
            
            append_to_json_file("product_urls.json", category, product_urls)
           
            if OFFSET is None:
                break
            time.sleep(3)
            
    
  
    

        
