import requests
import json
import xml.etree.ElementTree as ET
import re
import os

# Step 1: Access the sitemap index
sitemap_index_url = 'https://www.trendyol.com/sitemap_index.xml'
response = requests.get(sitemap_index_url)
root = ET.fromstring(response.content)

# Namespace dictionary for XML parsing
namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'image': 'http://www.google.com/schemas/sitemap-image/1.1',
    'xhtml': 'http://www.w3.org/1999/xhtml'}

# Step 2: Iterate through each sitemap URL
products_sitemap_urls = [elem.text for elem in root.findall('ns:sitemap/ns:loc', namespaces) \
                if re.search(r'^https://www\.trendyol\.com/sitemap_products.*\.xml$', elem.text)]

"""
with open ("product_urls.txt", "w") as file:
    for url in sitemap_urls:
        file.write(url+"\n")
"""
products = []


for sitemap_url in products_sitemap_urls[:3]:
    sitemap_response = requests.get(sitemap_url)
    sitemap_root = ET.fromstring(sitemap_response.content)
    
    for url_elem in sitemap_root.findall('ns:url', namespaces):
        product_url_elem = url_elem.find('ns:loc', namespaces)
        if product_url_elem is None:
            continue
        product_url = product_url_elem.text

    # Extract image URLs and titles
        images = []

        category = None

        image_elements = url_elem.findall('image:image', namespaces)
        for img in image_elements:
            img_url_elem = img.find('image:loc', namespaces)
            img_title_elem = img.find('image:title', namespaces)
            if img_url_elem is not None:
                images.append(img_url_elem.text)
            if img_title_elem is not None and category is None:
                category = img_title_elem.text  # Assuming title represents category

    # Append product data to the list
        products.append({
            'product_url': product_url,
            'category': category,
            'images': images
        })

# Save the data to a JSON file
with open('trendyol_products_image_urls.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

    
