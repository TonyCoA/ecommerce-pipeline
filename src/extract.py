import json
import requests

url = "https://dummyjson.com/products"
#url = "https://dummyjson.com/this-does-not-exist"

limit = 10
skip = 0
all_products = []

while True:
    params = {
        "limit": limit,
        "skip": skip
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        break

    data = response.json()
    products = data["products"]

    all_products.extend(products)

    print(
        f"Retrieved {len(products)} products "
        f"(skip={skip})"
    )

    if skip + limit >= data["total"]:
        break

    skip += limit

print("Total products retrieved:", len(all_products))

output_path = "data/raw/products.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(
        all_products,
        file,
        indent=2,
        ensure_ascii=False
    )

print(f"Saved {len(all_products)} products to {output_path}")