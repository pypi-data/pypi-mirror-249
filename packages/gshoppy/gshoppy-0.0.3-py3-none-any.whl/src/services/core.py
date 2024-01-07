"""
service.py contains the Service class, which is the base class for all services.
"""
from abc import ABC
from abc import abstractmethod
from typing import Generator
from typing import Sized

import google_auth_httplib2
import src.constants as constants
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient import http
from src.utils import get_logger
from src.utils import setup_logging

setup_logging()
logger = get_logger()


class Service(ABC):
    """
    The base class for all services.
    """

    def __init__(
        self,
        credentials: service_account.Credentials = None,
        merchant_id: str = None,
        sandbox: bool = False,
    ):
        """
        Initializes the service.

        :param sandbox: Whether to use the sandbox API.
        """

        self._sandbox = sandbox

        self._credentials = credentials
        self._merchant_id = merchant_id
        self._base_service = None

        # Initialize the service.
        self._service = None
        self._init_service()

    @property
    def sandbox(self) -> bool:
        """
        Whether this service uses the sandbox API.
        :return: Whether to use the sandbox API.
        """

        return self._sandbox

    @property
    def credentials(self) -> service_account.Credentials:
        """
        The service account credentials.
        :return:
        """

        if self._credentials is None:
            logger.warning(
                f"No credentials provided - defaulting to {constants.SERVICE_ACCOUNT_FILE}"
            )
            self._credentials = service_account.Credentials.from_service_account_file(
                constants.SERVICE_ACCOUNT_FILE, scopes=[constants.CONTENT_API_SCOPE]
            )

        return self._credentials

    @property
    def merchant_id(self) -> str:
        """
        The merchant ID.
        :return: The merchant ID.
        """

        if self._merchant_id is None:
            logger.warning(
                f"No merchant ID provided - defaulting to {constants.MERCHANT_ID}"
            )
            self._merchant_id = constants.MERCHANT_ID

        return self._merchant_id

    @property
    def base_service(self) -> discovery.Resource:
        """
        The base service.
        :return: The service.
        """

        if self._base_service is None:
            logger.info("Initializing the base service.")

            # Get the Auth HTTP for the service.
            http_arg = http.set_user_agent(
                http.build_http(), constants.APPLICATION_NAME
            )
            auth_http = google_auth_httplib2.AuthorizedHttp(
                self.credentials, http=http_arg
            )

            # Set service.
            self._base_service = discovery.build(
                constants.SERVICE_NAME,
                self.version,
                discoveryServiceUrl=constants.API_URI,
                http=auth_http,
            )

        return self._base_service

    @property
    def version(self) -> str:
        """
        The service version.
        :return: The service version.
        """

        return (
            constants.SANDBOX_SERVICE_VERSION
            if self.sandbox
            else constants.SERVICE_VERSION
        )

    @property
    def service(self) -> discovery.Resource:
        """
        The service.
        :return:
        """

        return self._service

    @staticmethod
    def _batch(iterable: Sized, size: int = constants.BATCH_SIZE) -> Generator:
        """
        Batches an iterable into chunks of a given size.
        :param iterable: The iterable to batch.
        :param size: The batch size.
        :return: The batched iterable.
        """

        for i in range(0, len(iterable), size):
            yield iterable[i : i + size]

    @abstractmethod
    def _init_service(self):
        """
        Initializes the service.
        :return:
        """

    def __del__(self):
        """
        Close any open service sockets.
        :return:
        """

        if self.service is not None:
            self.service.close()
        if self.base_service is not None:
            self.base_service.close()
