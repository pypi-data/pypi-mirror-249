"""
models.py contains the models for the application.
"""
from enum import Enum
from typing import Final

import gshoppy.constants as constants


class ProductAvailability(str, Enum):
    """
    The product availability.
    """

    IN_STOCK: Final[str] = constants.AVAILABILITY_IN_STOCK
    OUT_OF_STOCK: Final[str] = constants.AVAILABILITY_OUT_OF_STOCK
    PREORDER: Final[str] = constants.AVAILABILITY_PREORDER
