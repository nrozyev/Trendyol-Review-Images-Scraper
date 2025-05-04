import json

with open("download.json") as f:
    data = json.load(f)
    products = data.get("products", [])
    keys = data.keys()
    widgets = data.get("widgets", [])

print(len(widgets))
