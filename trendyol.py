import requests
import xml.etree.ElementTree as ET
import json

# Step 1: Download the XML content
url = 'https://www.trendyol.com/sitemap_products79.xml'
response = requests.get(url)
response.raise_for_status()  # Ensure we notice bad responses

# Step 2: Parse the XML content
root = ET.fromstring(response.content)

# Step 3 and 4: Extract data and write to JSONL
with open('sitemap_products79.jsonl', 'w', encoding='utf-8') as jsonl_file:
    for url_element in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url_element.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        lastmod = url_element.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
        data = {
            'loc': loc.text if loc is not None else None,
            'lastmod': lastmod.text if lastmod is not None else None
        }
        jsonl_file.write(json.dumps(data) + '\n')
