"""
utils.py contains utility functions used throughout the application.
"""
import logging

import gshoppy.constants as constants
from google.oauth2 import service_account


def setup_logging() -> None:
    """
    Sets up logging.
    :return:
    """

    # Set up basic config.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def get_logger() -> logging.Logger:
    """
    Gets the logger.
    :return:
    """

    return logging.getLogger()


def get_product_id(offer_id: str) -> str:
    """
    Get the product ID from the offer ID.
    :param offer_id: The offer ID.
    :return: The product ID.
    """

    return f"{constants.CHANNEL}:{constants.CONTENT_LANGUAGE}:{constants.TARGET_COUNTRY}:{offer_id}"


def get_credentials_from_file(path: str) -> service_account.Credentials:
    """
    Loads credentials from a file.
    :param path:
    :return:
    """

    return service_account.Credentials.from_service_account_file(
        path, scopes=[constants.CONTENT_API_SCOPE]
    )
