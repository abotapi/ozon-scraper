# Ozon Scraper

**Get Ozon.ru products as JSON or CSV: prices, discounts, ratings, reviews, specs, variants, the current seller and every competing seller (buybox), by keyword or by product, category, search or seller URL.**

![Output](https://img.shields.io/badge/output-JSON%20%7C%20CSV%20%7C%20Excel-green?style=flat-square)
![Country](https://img.shields.io/badge/country-Russia-blue?style=flat-square)
![License](https://img.shields.io/badge/examples-MIT-lightgrey?style=flat-square)

Ozon is Russia's largest online marketplace. Thousands of sellers often compete on the same product card, so price
and seller data changes daily. Ozon's Seller API only covers your own shop; for competitors, categories and reviews you
need the public site.

This repo shows how to pull that data with the
**[Ozon.ru Scraper on Apify](https://apify.com/abotapi/ozon-ru-scraper?utm_source=github&utm_medium=ozon-scraper&utm_campaign=showcase)**,
a hosted scraper you can run from the web UI or call from code.

## Table of Contents

- [What you can get](#what-you-can-get)
- [Quick start](#quick-start)
- [Examples](#examples)
- [Input options](#input-options)
- [Sample output](#sample-output)
- [Use cases](#use-cases)
- [FAQ](#faq)

## What you can get

| Group | Fields |
| --- | --- |
| **Product** | SKU, URL, title, brand, price, original price, discount %, price strings (`5 190 ₽`), currency, rating, rating breakdown (1–5 stars), review and question counts, stock text, category path, hashtags |
| **Details** (default on) | description, specs, image gallery, variants (color, size, ... with their own SKU, price and stock) |
| **Seller** | current seller with rating, order count and premium flag |
| **Buybox** (default on) | every competing seller on the same product with delivery date and authorized-brand flag; other sellers' count and lowest price |
| **Reviews** (`fetchReviews`) | author, score, text, pros/cons, photos, videos, helpful votes, publish time |

## Quick start

**No code:** open the [scraper page](https://apify.com/abotapi/ozon-ru-scraper?utm_source=github&utm_medium=ozon-scraper&utm_campaign=showcase),
type a search term (Russian works best, e.g. `наушники` for "headphones"), click **Start**, and download JSON, CSV or Excel.

**From code:** get a free [Apify API token](https://console.apify.com/settings/integrations?utm_source=github&utm_medium=ozon-scraper&utm_campaign=showcase), then:

```bash
git clone https://github.com/abotapi/ozon-scraper && cd ozon-scraper
export APIFY_TOKEN=<your token>
```

> **Use a residential proxy.** Every example sets
> `"proxy": {"useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"]}`. Leave the country empty.

## Examples

### Python: keyword search, saved to CSV

[`examples/python/main.py`](examples/python/main.py)

```bash
pip install "apify-client>=3"
python examples/python/main.py "наушники"
```

```text
Saved 10 products to ozon.csv
- Наушники беспроводные SampleAudio Air Pro с шумоподавлением, бел | 4 990 ₽ | rating 4.8 | seller Пример Электроникс
- Наушники накладные DemoSound 300, черные | 2 390 ₽ | rating 4.7 | seller Демо Дом
```

### Node.js: buybox tracker

[`examples/node/index.mjs`](examples/node/index.mjs) walks a search results URL and lists who else sells each product, with delivery dates.

```bash
cd examples/node && npm install && node index.mjs
```

```text
5 products
Робот-пылесос ExampleClean R5, влажная уборка, Wi-Fi | 12 490 ₽ | sold by Пример Электроникс | 3 other sellers
   - Магазин Образец: Доставим 18 октября
   - Демо Дом: Доставим 21 октября
```

(Printed values above are mock.)

### cURL: biggest discounts, search fields only

[`examples/curl.sh`](examples/curl.sh) sorts by discount and turns `scrapeProductDetails` off, which returns only search-result fields and is much faster and cheaper:

```bash
./examples/curl.sh > discounts.json
```

## Input options

| Option | What it does |
| --- | --- |
| `mode` | `search` (keywords) or `url` (product, category, search or seller URLs) |
| `queries` | Search terms in Russian or English |
| `urls` | Full `https://www.ozon.ru/` product, `/category/`, `/search/` or `/seller/` URLs (short `ozon.ru/t/` links are not supported) |
| `sortBy` | `score` (relevance), `price`, `price_desc`, `new`, `rating`, `discount` |
| `minPrice` / `maxPrice` / `minRating` | Filters (prices in RUB) |
| `scrapeProductDetails` | On by default: description, specs, gallery, variants, seller, category. Off: search-result fields only |
| `fetchBuybox` / `fetchSellerDetails` | Competing sellers / seller profile data (both on by default) |
| `fetchReviews` / `maxReviewsPerProduct` | Attach customer reviews to each product |
| `maxListings` / `maxPages` / `maxItems` | Limit results |
| `incrementalMode` | For scheduled runs: only output new or changed products, e.g. price changes |

See the [scraper page](https://apify.com/abotapi/ozon-ru-scraper?utm_source=github&utm_medium=ozon-scraper&utm_campaign=showcase) for the full list.

## Sample output

Mock data with the same fields and types as real output (the products, sellers and reviews are made up):
[`sample-output/sample.json`](sample-output/sample.json) · [`sample-output/sample.csv`](sample-output/sample.csv)

```json
{
  "sku": "9000000001",
  "title": "Наушники беспроводные SampleAudio Air Pro с шумоподавлением, белые",
  "brand": "SampleAudio",
  "price": 4990,
  "originalPrice": 8990,
  "discountPercent": 44,
  "priceString": "4 990 ₽",
  "currency": "RUB",
  "rating": 4.8,
  "reviewCount": 3120,
  "ratingBreakdown": { "1": 40, "2": 25, "3": 90, "4": 410, "5": 2555 },
  "availability": "12 ед осталось",
  "categoryPath": "Электроника > Наушники и аудиотехника > Наушники",
  "sellerName": "Пример Электроникс",
  "otherSellersCount": 3,
  "otherSellersMinPrice": 4790,
  "buyboxSellers": [
    { "name": "Магазин Образец", "deliveryText": "Доставим 18 октября", "authorizedSeller": "Проверенный продавец бренда", "productSku": "9000000011" }
  ],
  "url": "https://www.ozon.ru/product/naushniki-besprovodnye-sampleaudio-air-pro-9000000001"
}
```

## Use cases

- **Price monitoring:** daily prices and discounts for your products or competitors', with `incrementalMode`
- **Buybox and reseller control:** which sellers offer a brand's products, at what delivery speed, and whether they are authorized
- **Assortment research:** brands, price bands and specs that win a category
- **Review analysis:** ratings and review text across a category for product development
- **AI and data teams:** structured Russian e-commerce data for product matching and RAG

## FAQ

**How much does it cost?** You pay per result on Apify, and new accounts get free monthly credit. See the scraper page for current pricing. Residential proxy traffic is billed by Apify separately.

**Russian or English queries?** Both work. Russian queries (`наушники`, `кроссовки`) match how Ozon shoppers search. For a search URL, URL-encode the Cyrillic text, as in the Node example.

**Why are there duplicate field names?** `specs`/`specifications`, `seller`/`sellerInfo` and `reviewCount`/`reviewsCount` hold the same data, so code written for other Ozon scrapers keeps working.

**Is scraping Ozon allowed?** The scraper only collects publicly visible product, seller and review data. Check Ozon's terms and applicable law for your use case.

## Related

- [Awesome Web Scrapers](https://github.com/abotapi/abotapi): a curated list of ready-to-run scrapers, including other Russian sites ([Avito](https://github.com/abotapi/avito-scraper), Wildberries, Cian)
- [web-scrapers](https://github.com/abotapi/web-scrapers): code examples and mock samples for every scraper in that list

---

<sub>The scraper is maintained by [abotapi](https://abotapi.com/?utm_source=github&utm_medium=ozon-scraper&utm_campaign=showcase). Examples in this repo are MIT licensed. Not affiliated with Ozon.</sub>
