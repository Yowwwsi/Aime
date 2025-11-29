# Aime Discovery Backend Outline

This document maps the product spec into a small, testable backend slice that can power the guided shopping conversation and 4-card grid.

## Intent capture
The `Intent` dataclass in `aime/intent.py` stores the normalized request so the assistant can collect only missing fields:
- `category`, `price_min`, `price_max`
- `constraints` (e.g., wireless, waterproof, RGB)
- `keywords` (brands, style words, colors)
- `is_gift`, `gift_recipient_age_range`, `relationship`
- `geo_mode` (local or global), `country`, `currency`

Helper: `matches_price` keeps price filtering logic centralized.

## Search abstraction
`SearchProvider` defines the common interface used by the conversation and UI layers:
- `search_products(intent, limit=4)` returns the four best cards to show at once.
- `get_product_details(product_id)` supports opening/saving/sharing actions.

`Product` normalizes store data: ids, names, media, price, rating, highlight bullets, geo, and optional affiliate tags for monetization.

## MVP_FAKE implementation
`FakeSearchProvider` loads `data/products.json` and applies lightweight ranking:
1. Filter by category and price.
2. Respect geo mode: local means origin matches the selected country; global means the country must appear in `ships_to`.
3. Require constraint tags when provided.
4. Encourage keyword overlap; sort primarily by rating, then by keyword coverage.

This keeps the experience snappy and predictable while mimicking the eventual web-backed provider.

## Extending toward WEB_LIVE
- Swap `FakeSearchProvider` with a network-backed provider that maps API responses into the `Product` model.
- Add short-lived caching keyed by normalized intent to keep the perceived latency near two seconds.
- Enrich analytics hooks around `product_opened`, `product_saved`, and `product_shared` events before emitting to telemetry.
