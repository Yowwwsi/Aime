from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Intent:
    category: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    constraints: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    is_gift: bool = False
    gift_recipient_age_range: Optional[str] = None
    relationship: Optional[str] = None
    geo_mode: Optional[str] = None  # "local" or "global"
    country: Optional[str] = None  # IL / US / UK
    currency: Optional[str] = None

    def matches_price(self, price: float) -> bool:
        if self.price_min is not None and price < self.price_min:
            return False
        if self.price_max is not None and price > self.price_max:
            return False
        return True
