# Sample output

**Mock data.** These records have the same fields and types as real scraper output, but every value is made up: the products, brands, sellers, reviewers, SKUs and URLs are fictional. They show the structure only.

- `sample.json`: products with full details, buybox sellers and reviews (`fetchReviews: true`)
- `sample.csv`: the flat (non-nested) fields of the same records

`specs`/`specifications`, `seller`/`sellerInfo` and `reviewCount`/`reviewsCount` carry the same data under two names, so code written for other Ozon scrapers keeps working.
