import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

from aime.intent import Intent
from aime.search_provider import Product, SearchProvider

DATA_PATH = Path(__file__).resolve().parent.parent / ".." / "data" / "products.json"


@dataclass
class CatalogProduct:
    id: str
    category: str
    name: str
    image_url: str
    price: float
    currency: str
    rating: float
    review_count: int
    store_name: str
    store_url: str
    highlights: List[str]
    tags: List[str]
    origin_country: str
    ships_to: List[str]
    affiliate_tag: str | None

    def to_product(self) -> Product:
        return Product(
            id=self.id,
            name=self.name,
            image_url=self.image_url,
            price=self.price,
            currency=self.currency,
            rating=self.rating,
            review_count=self.review_count,
            store_name=self.store_name,
            store_url=self.store_url,
            highlights=self.highlights,
            geo=self.origin_country,
            affiliate_tag=self.affiliate_tag,
        )


class FakeSearchProvider(SearchProvider):
    def __init__(self, data_path: Path | None = None):
        path = data_path or DATA_PATH
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        self.catalog = [CatalogProduct(**item) for item in raw]

    def search_products(self, intent: Intent, limit: int = 4) -> List[Product]:
        filtered = [item for item in self.catalog if self._matches_intent(item, intent)]
        filtered.sort(key=lambda item: (-item.rating, -self._keyword_score(item, intent)))
        products = [item.to_product() for item in filtered[:limit]]
        return products

    def get_product_details(self, product_id: str) -> Product:
        for item in self.catalog:
            if item.id == product_id:
                return item.to_product()
        raise KeyError(f"Product {product_id} not found")

    def _matches_intent(self, item: CatalogProduct, intent: Intent) -> bool:
        if intent.category and item.category != intent.category:
            return False
        if intent.geo_mode == "local" and intent.country:
            if item.origin_country != intent.country:
                return False
        if intent.geo_mode == "global" and intent.country:
            if intent.country not in item.ships_to:
                return False
        if not intent.matches_price(item.price):
            return False
        if intent.constraints:
            if not all(constraint.lower() in (tag.lower() for tag in item.tags) for constraint in intent.constraints):
                return False
        if intent.keywords:
            keyword_hits = [kw for kw in intent.keywords if kw.lower() in (tag.lower() for tag in item.tags)]
            if not keyword_hits:
                return False
        return True

    def _keyword_score(self, item: CatalogProduct, intent: Intent) -> float:
        if not intent.keywords:
            return 0
        matches = 0
        for kw in intent.keywords:
            if kw.lower() in (tag.lower() for tag in item.tags):
                matches += 1
        return matches / len(intent.keywords)
