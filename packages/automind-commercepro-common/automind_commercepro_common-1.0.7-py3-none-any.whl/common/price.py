from pydantic import Field
from common.offer import Offer
from common.utility import get_isoformat
from typing import Any, Optional
from common.model import Model


class Price(Model):
    """Represents a price."""

    id: Optional[int] = None
    price: float
    offer: Offer
    is_locked: bool = False
    vat_rate: float = 0.22
    discount_rate: float = 0.0

    created_at: str = Field(default_factory=get_isoformat)
    expired_at: Optional[str] = None
    is_supplier_locked: bool = False

    def model_dto(self) -> dict:
        dto = super().model_dto()
        dto["offer_id"] = self.offer.id
        del dto["offer"]
        return dto
