from typing import Literal, Optional
from pydantic import BaseModel
from common.model import Model


class Supplier(Model):
    id: int
    name: str
    offers_url: str
    min_processing_days: int = 3
    max_processing_days: int = 5
    reliability: Literal["high", "medium", "low"] = "medium"
    is_internal: bool = False
    is_dropshipper: bool = False
    is_active: bool = False


class SupplierOffer(BaseModel):
    """Represents a lightweight `Supplier` offer."""

    sku: str
    ean: Optional[str] = None
    mpn: Optional[str] = None
    title: Optional[str] = None
    brand_name: Optional[str] = None
    price: float
    quantity: int = 0
    discount_rate: float = 0.0
    images: Optional[list[str]] = None
    vat_rate: float = 0.0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SupplierOffer):
            return False

        return (
            self.sku == other.sku
            and self.price == other.price
            and self.quantity == other.quantity
            and self.discount_rate == other.discount_rate
            and self.vat_rate == other.vat_rate
        )
