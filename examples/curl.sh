#!/usr/bin/env bash
# Biggest discounts for a keyword, search-result fields only (fast and cheap), in one HTTP call.
# APIFY_TOKEN=<your token> ./curl.sh > discounts.json
curl -s -X POST \
  "https://api.apify.com/v2/acts/abotapi~ozon-ru-scraper/run-sync-get-dataset-items?token=${APIFY_TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "mode": "search",
    "queries": ["кроссовки"],
    "sortBy": "discount",
    "scrapeProductDetails": false,
    "maxListings": 20,
    "proxy": { "useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"] }
  }'
