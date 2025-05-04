import os
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import time

def fetch_url(url, timeout=50, retry_delay=5):
    while True:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

# Define the sitemap index URL
sitemap_index_url = 'https://www.trendyol.com/sitemap_index.xml'

# Create a directory to store downloaded sitemaps
base_output_dir = 'trendyol_sitemaps'
os.makedirs(base_output_dir, exist_ok=True)

language_codes = ['hu', 'pl', 'el']


# Fetch the sitemap index
response = requests.get(sitemap_index_url)
response.raise_for_status()  # Ensure we notice bad responses

# Parse the XML content
root = ET.fromstring(response.content)

# Define the namespace
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Find all sitemap locations
sitemap_urls = [elem.text for elem in root.findall('ns:sitemap/ns:loc', namespace)]

# Download each sitemap
for sitemap_url in sitemap_urls:
    print(f'Downloading: {sitemap_url}')
    sitemap_response = fetch_url(sitemap_url)
    sitemap_response.raise_for_status()
    
    # Determine the filename from the URL
    parsed_url = urlparse(sitemap_url)
    path_parts = parsed_url.path.strip('/').split('/')

     # Determine if any language code is present in the path
    subdirectory = ''
    if len(path_parts) > 1:
        potential_lang = path_parts[0]
        if len(potential_lang) == 2 and potential_lang.isalpha():
            subdirectory = potential_lang
    
    # Set the output directory
    output_dir = os.path.join(base_output_dir, subdirectory) if subdirectory else base_output_dir
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine the filename from the URL
    filename = os.path.basename(parsed_url.path)
    filepath = os.path.join(output_dir, filename)
    
    # Save the sitemap content to a file
    with open(filepath, 'wb') as file:
        file.write(sitemap_response.content)
    
    print(f'Saved to: {filepath}')


