from typing import Literal, Optional
from pydantic import BaseModel, Field
from common.supplier import SupplierOffer, Supplier


class OfferDiff(BaseModel):
    """Class to represent the difference between two products."""

    offer: Optional[SupplierOffer] = None
    old_offer: Optional[SupplierOffer] = None
    type: Literal["new", "removed", "updated"]


class Catalogue(BaseModel):
    """Class to represent a catalogue."""

    supplier: Supplier
    offers: dict[str, SupplierOffer]


class CatalogueDiff(BaseModel):
    """Class to represent the difference between two catalogues."""

    supplier: Supplier
    diff: list[OfferDiff] = Field(default_factory=list)
