from typing import Literal, Optional
from pydantic import Field
from common.product import Variant
from common.supplier import Supplier
from common.utility import get_isoformat
from common.model import Model


class Offer(Model):
    """Represents an offer."""

    id: Optional[int] = None
    price: float
    supplier: Supplier
    variant: Variant
    supplier_sku: str
    quantity: int = 0
    currency: Literal["eur", "usd"] = "eur"
    vat_rate: float = 0.22
    discount_rate: float = 0.0
    max_processing_days: Optional[int] = None
    min_processing_days: Optional[int] = None

    created_at: str = Field(default_factory=get_isoformat)
    expired_at: Optional[str] = None

    def model_dto(self) -> dict:
        dto = super().model_dto()
        dto["supplier_id"] = self.supplier.id
        del dto["supplier"]
        dto["variant_id"] = self.variant.id
        del dto["variant"]
        return dto
