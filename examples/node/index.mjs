// Buybox tracker: who else sells the same Ozon products, and at what delivery date.
// npm install && APIFY_TOKEN=<your token> node index.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('abotapi/ozon-ru-scraper').call({
    mode: 'url',
    urls: ['https://www.ozon.ru/search/?text=%D1%80%D0%BE%D0%B1%D0%BE%D1%82+%D0%BF%D1%8B%D0%BB%D0%B5%D1%81%D0%BE%D1%81'], // "robot vacuum"; any product, category, search or seller URL
    fetchBuybox: true,
    maxListings: 5,
    proxy: { useApifyProxy: true, apifyProxyGroups: ['RESIDENTIAL'] },
}, { log: null }); // don't stream the run log to your console

const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(`${items.length} products`);
for (const p of items) {
    console.log(`${p.title.slice(0, 60)} | ${p.priceString} | sold by ${p.sellerName} | ${p.otherSellersCount} other sellers`);
    for (const s of (p.buyboxSellers ?? []).slice(0, 3)) {
        console.log(`   - ${s.name}: ${s.deliveryText ?? ''}`);
    }
}
