"""
product.py contains the Product service class.
"""
from abc import ABC
from typing import Generator
from typing import List

import src.constants as constants
from src.services.core import Service
from src.utils import get_logger
from src.utils import get_product_id
from src.utils import setup_logging

setup_logging()
logger = get_logger()


class ProductService(Service, ABC):
    """
    The Product service class.
    """

    def _init_service(self):
        """
        Initializes the Product Service.
        :return:
        """

        logger.info("Initializing the Product service.")

        self._service = self.base_service.products()

    def get(self, offer_id: str) -> dict:
        """
        Gets a product.
        :param offer_id: The offer ID of the product to get.
        :return:
        """

        logger.info("Getting product.")

        # Get the product ID.
        product_id = get_product_id(offer_id)

        # Build a request.
        request = self.service.get(merchantId=self.merchant_id, productId=product_id)

        # Execute the request.
        return request.execute()

    def list(self) -> Generator:
        """
        Yield out pages of products.
        :return:
        """

        logger.info("Fetching products")

        # Build a request.
        request = self.service.list(
            merchantId=self.merchant_id, maxResults=constants.MAX_PAGE_SIZE
        )

        # Get all pages.
        while request is not None:
            # Execute the request.
            response = request.execute()

            # Yield the products.
            yield response.get("resources")

            # Update the request.
            request = self.service.list_next(
                previous_request=request, previous_response=response
            )

    def insert(self, **product) -> dict:
        """
        Inserts a product.
        :param product: The product to insert.
        :return:
        """

        logger.info("Inserting product.")

        # Build a request.
        request = self.service.insert(merchantId=self.merchant_id, body=product)

        # Execute the request.
        return request.execute()

    def update(self, offer_id: str, **product) -> dict:
        """
        Updates a product.
        :param offer_id:
        :param product:
        :return:
        """

        logger.info("Updating product.")

        # Get the product.
        _product = self.get(offer_id)

        # Update the product.
        _product.update(product)

        # Cannot specify `source` when inserting a product.
        del _product["source"]

        # Re-insert the product.
        return self.insert(**_product)

    def delete(self, offer_id: str) -> None:
        """
        Deletes a product.
        :param offer_id: The offer ID of the product to delete.
        :return:
        """

        logger.info("Deleting product.")

        # Get the product ID.
        product_id = get_product_id(offer_id)

        # Build a request.
        request = self.service.delete(merchantId=self.merchant_id, productId=product_id)

        # Execute the request.
        request.execute()

    def batch_insert(
        self, *products: List[dict], batch_size: int = constants.BATCH_SIZE
    ):
        """
        Inserts products in batches.
        :param products:
        :param batch_size:
        :return:
        """

        raise NotImplementedError()

    def batch_delete(
        self, *offer_ids: List[str], batch_size: int = constants.BATCH_SIZE
    ):
        """
        Deletes products in batches.
        :param offer_ids:
        :param batch_size:
        :return:
        """

        raise NotImplementedError()
