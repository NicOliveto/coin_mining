from .storage_base import StorageBase
from app.resources.database_resource import DatabaseResource, CoinDataResource
import logging

class PostgresStorage(StorageBase):
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.logger = logging.getLogger(__name__)

    def save(self, data: list):
        try:
            self.logger.info("Connecting to database...")
            db_resource = DatabaseResource(self.database_url)
            coin_data_resource = CoinDataResource(db_resource)

            self.logger.info("Inserting records into the database")
            coin_data_resource.insert_bulk_coin_prices(data)

            self.logger.info("Data updated on postgres")
        except Exception as e:
            self.logger.exception(f"Error writing data on postgres")
            raise RuntimeError(f"Error writing data on postgres: {str(e)}")