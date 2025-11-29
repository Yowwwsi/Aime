# Aime

Aime is a mobile-first, voice-led shopping companion featuring a playful cloud avatar. This repo holds early backend experiments for intent modeling and catalog search that power the guided conversation and 4-card result grid.

## Structure
- `aime/intent.py` – intent dataclass capturing user needs (category, budget, geo, gift hints, and keywords).
- `aime/search_provider.py` – shared `Product` model and `SearchProvider` protocol.
- `aime/providers/fake_provider.py` – MVP_FAKE provider using a local catalog with simple ranking and geo-aware filtering.
- `data/products.json` – seed catalog spanning core categories (sneakers, hoodies, headphones, jeans, skincare, gaming, accessories).

## Quick demo
Run a tiny search against the fake provider:

```bash
python - <<'PY'
from aime.intent import Intent
from aime.providers.fake_provider import FakeSearchProvider

provider = FakeSearchProvider()
intent = Intent(category="headphones", price_max=60, keywords=["wireless"], geo_mode="local", country="US")
results = provider.search_products(intent)
for product in results:
    print(product)
PY
```

This filters by category, budget, geo preference, and keyword overlap, returning up to four products ranked by rating and keyword match.
