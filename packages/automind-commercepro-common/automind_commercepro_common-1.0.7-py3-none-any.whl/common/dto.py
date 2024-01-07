from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, field_serializer


class VariantDTO(BaseModel):
    id: str
    ean: str


class OfferDTO(BaseModel):
    id: Optional[int] = None
    price: float
    quantity: int
    supplier_id: int
    variant_id: uuid.UUID
    supplier_sku: str
    vat_rate: float
    discount_rate: float
    expired_at: Optional[datetime] = None


class OfferPriceDTO(BaseModel):
    variant_id: uuid.UUID
    offer_id: int
    supplier_id: int
    supplier_sku: str
    offer_price: float
    offer_vat_rate: float
    offer_discount_rate: float
    offer_quantity: int
    price_id: Optional[int]
    price_value: Optional[float]


class PriceDTO(BaseModel):
    id: Optional[int] = None
    offer_id: int
    is_locked: bool
    price: float
    vat_rate: float
    discount_rate: float
    is_supplier_locked: bool = False


class PriceLockDTO(BaseModel):
    id: Optional[int] = None
    variant_id: uuid.UUID
    price: float
    discount_rate: float


class SupplierLockDTO(BaseModel):
    id: Optional[int] = None
    supplier_id: int
    variant_id: uuid.UUID


class SupplierDTO(BaseModel):
    id: int
    name: str
    min_processing_days: int
    max_processing_days: int
    reliability: str
    is_internal: bool
    is_dropshipper: bool
    offers_url: str
    is_active: bool
