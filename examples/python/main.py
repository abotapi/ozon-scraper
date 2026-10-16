"""Search Ozon.ru products and save prices, ratings and sellers to CSV.

pip install "apify-client>=3"
APIFY_TOKEN=<your token> python main.py "наушники"
"""
import csv
import os
import sys

from apify_client import ApifyClient

queries = sys.argv[1:] or ["наушники"]  # "headphones"; English queries work too
client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("abotapi/ozon-ru-scraper").call(run_input={
    "mode": "search",
    "queries": queries,
    "sortBy": "score",           # relevance; also price, price_desc, new, rating, discount
    "maxListings": 10,
    "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
}, logger=None)  # logger=None: don't stream the run log to your console

items = list(client.dataset(run.default_dataset_id).iterate_items())
fields = ["sku", "title", "brand", "price", "originalPrice", "discountPercent", "rating", "reviewCount",
          "sellerName", "otherSellersCount", "otherSellersMinPrice", "categoryPath", "url"]
with open("ozon.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(items)

print(f"Saved {len(items)} products to ozon.csv")
for it in items[:5]:
    print(f"- {it['title'][:60]} | {it.get('priceString')} | rating {it.get('rating')} | seller {it.get('sellerName')}")
