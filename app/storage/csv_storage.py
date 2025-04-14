import csv
import logging
from .storage_base import StorageBase

class CSVStorage(StorageBase):
    def __init__(self, file_name: str):
        self.filename = file_name
        self.logger = logging.getLogger(__name__)

    def save(self, data: list) -> None:
        """Saves the provided data into a csv file located in the specified data path"""
        self.logger.info(f"Starting to save data to {self.filename}")
        try:
            with open(self.filename, mode="a", newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            self.logger.info(f"Data saved to {self.filename}")
        except OSError as e:
            self.logger.exception(f"Error saving data to {self.filename}")
            raise RuntimeError(f"Failed to save data to {self.filename}: {e}")
