"""
models.py contains the models for the application.
"""

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Final, Optional

import gshoppy.constants as constants


class ProductAvailability(str, Enum):
    """
    The product availability.
    """

    IN_STOCK: Final[str] = constants.AVAILABILITY_IN_STOCK
    OUT_OF_STOCK: Final[str] = constants.AVAILABILITY_OUT_OF_STOCK
    PREORDER: Final[str] = constants.AVAILABILITY_PREORDER


class Currency(str, Enum):
    """
    Supported currencies.
    """

    USD: Final[str] = "USD"


class Country(str, Enum):
    """
    Supported countries.
    """

    US: Final[str] = "US"


class Channel(str, Enum):
    """
    Supported channels.
    """

    ONLINE: Final[str] = "online"
    LOCAL: Final[str] = "local"


class Product(BaseModel):
    """
    The ``Product`` model represents a product in
    Google Shopping.
    ** Note - The fields defined here are only the required
    fields as defined by Googl - Additional fields are optional. **
    """

    title: Optional[str] = Field(default=None, description="The title of the item.")
    availability: ProductAvailability = Field(
        default=constants.AVAILABILITY_IN_STOCK,
        description="The availability of the item.",
    )
    channel: Optional[str] = Field(
        default=constants.CHANNEL, description="The item's channel (online or local)."
    )
    contentLanguage: str = Field(
        default=constants.CONTENT_LANGUAGE,
        description="The two-letter ISO 639-1 language code for the item.",
    )
    offerId: Optional[str] = Field(
        ...,
        description="""
            A unique identifier for the item. Leading and trailing whitespaces are stripped and multiple whitespaces
            are replaced by a single whitespace upon submission. Only valid unicode characters are accepted. See the
            products feed specification for details. *Note:* Content API methods that operate on products take the
            REST ID of the product, *not* this identifier.
        """,
    )
    targetCountry: Optional[str] = Field(
        default=constants.TARGET_COUNTRY,
        description="The CLDR territory code for the item's country of sale.",
    )

    # Config for model.
    model_config = ConfigDict(extra="allow")


class Price(BaseModel):
    """
    The ``Price`` model represents the price of a product.
    """

    value: Final[str] = Field(..., description="The price represented as a number.")
    currency: Final[str] = Field(..., description="The currency of the price.")


class ProductShipping(BaseModel):
    """
    The ``ProductShipping`` model represents the shipping information
    for a product.
    """

    country: Final[Country] = Field(
        ...,
        description="The CLDR territory code of the country to which an item will ship.",
    )
    service: Final[str] = Field(..., description="The name of the shipping service.")
    price: Final[Price] = Field(..., description="The price of the shipping service.")
