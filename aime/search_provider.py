from dataclasses import dataclass
from typing import List, Protocol

from .intent import Intent


@dataclass
class Product:
    id: str
    name: str
    image_url: str
    price: float
    currency: str
    rating: float
    review_count: int
    store_name: str
    store_url: str
    highlights: List[str]
    geo: str
    affiliate_tag: str | None = None


class SearchProvider(Protocol):
    def search_products(self, intent: Intent, limit: int = 4) -> List[Product]:
        ...

    def get_product_details(self, product_id: str) -> Product:
        ...
