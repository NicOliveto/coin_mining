from app.clients.awesome_api_client import AwesomeApiClient
from app.clients.api_client import ApiClient
import logging

logger = logging.getLogger(__name__)

class ClientFactory:
    @staticmethod
    def get_client(api_name: str, clients=None) -> ApiClient:

        clients = clients or {
            "awesomeapi": AwesomeApiClient
        }

        client_class = clients.get(api_name)

        if not client_class:
            raise ValueError(f"Unsopported client type: {api_name}. Available types: {", ".join(clients.keys())}" )

        return client_class()
