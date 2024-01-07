import re
from typing import Literal, Optional, List
from pydantic import PositiveFloat, PositiveInt, field_validator
from common.model import Model


class Brand(Model):
    """Represents a Brand."""

    id: Optional[int] = None
    name: str


class Taxonomy(Model):
    """Represents a Taxonomy."""

    id: Optional[int] = None
    path: str


class Product(Model):
    """Common data between a Simple and a Variant product."""

    id: Optional[str] = None
    type: Literal["simple", "variant"] = "simple"
    brand: Optional[Brand] = None
    title: Optional[str] = None
    micro_description: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    taxonomy: Optional[Taxonomy] = None
    raw_specs: Optional[dict] = None

    def model_dto(self) -> dict:
        dto = super().model_dto()
        dto["brand_id"] = self.brand.id if self.brand.id else None
        del dto["brand"]
        dto["taxonomy_id"] = self.taxonomy.id if self.taxonomy.id else None
        del dto["taxonomy"]
        return dto


class Attribute(Model):
    """Represents a Product Attribute."""

    id: Optional[PositiveInt] = 0
    name: str
    type: Literal["string", "integer", "float"]


class AttributeValue(Model):
    """Represents a Product Attribute Value."""

    value: str | PositiveInt | PositiveFloat
    attribute: Attribute

    def model_dto(self) -> dict:
        dto = super().model_dto()
        dto["attribute_id"] = self.attribute.id if self.attribute.id else None
        del dto["attribute"]
        return dto


class Variant(Model):
    """Variant-specific data linked to a parent `Product`."""

    id: str
    product: Product
    ean: str
    mpn: Optional[str] = None
    title: Optional[str] = None
    images: Optional[List[str]] = None
    weight_grams: Optional[PositiveFloat] = None
    height_centimeters: Optional[PositiveFloat] = None
    width_centimeters: Optional[PositiveFloat] = None
    depth_centimeters: Optional[PositiveFloat] = None
    attributes: Optional[list[AttributeValue]] = None
    raw_specs: Optional[dict] = None

    def get_search_string(self) -> str:
        """"""
        search_string = ""
        if self.title:
            search_string += self.title
        if self.product.title:
            search_string += self.product.title
        if self.mpn:
            search_string += " " + self.mpn
        if self.ean:
            search_string += " " + self.ean
        if self.product.id:
            search_string += " " + self.product.id
        if self.product.taxonomy:
            search_string += " " + self.product.taxonomy.path
        return search_string

    @field_validator("ean")
    @classmethod
    def ean_must_be_valid(cls, v):
        """Validates the EAN."""

        digit_regex = r"^\d{13}$"
        if not re.match(digit_regex, v):
            raise ValueError("Invalid EAN.")
        return v

    def model_dto(self) -> dict:
        dto = super().model_dto()
        dto["product_id"] = self.product.id if self.product.id else None
        del dto["product"]
        if dto.get("attributes"):
            del dto["attributes"]
        dto["search_string"] = self.get_search_string()
        return dto
