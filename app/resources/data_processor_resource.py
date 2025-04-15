import asyncio
import logging
import aiohttp
from datetime import datetime, timezone, timedelta
from app.clients.api_client import ApiClient
from app.storage.storage_base import StorageBase


class DataProcessorResource:
    def __init__(self, client: ApiClient, storage: StorageBase, concurrency_limit: int):
        self.client = client
        self.storage = storage
        self.logger = logging.getLogger(__name__)
        self.semaphore = asyncio.Semaphore(concurrency_limit)

    @staticmethod
    def __get_days_quantity(start_date: str, end_date: str) -> int:
        """Calculate the dates from start_date to end_date."""
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except:
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")

        days_qty = 0
        delta = end_date - start_date
        for i in range(delta.days + 1):
            days_qty += 1

        if days_qty > 360:
            raise ValueError("No more than 360 days can be drawn at any one time.")

        logging.info(f"Generated days qty: {days_qty}")
        return days_qty

    async def __fetch_historical_price(self, currency: str, start_date: str, end_date: str, days: int):
        """
        Fetches the historical price of a specific currency for a given period of time using
        the specified API client.
        """
        async with self.semaphore:
            try:
                self.logger.info(f"Fetching historial price for {currency} from {start_date} to {end_date}")
                data = await self.client.get_historical_price(currency, start_date, end_date, days)
                if not data:
                    raise ValueError("No data returned from the API.")
                data_list = []
                for item in data:
                    data_list.append({
                         "base_currency_id": str(data[0]["code"])
                        ,"target_currency_id": str(data[0]["codein"])
                        , "date_time": datetime.fromtimestamp(int(item["timestamp"]), tz=timezone.utc).strftime(
                            '%Y-%m-%d %H:%M:%S')
                        ,"purchase_amt": float(item["bid"])
                        ,"sale_amt": float(item["ask"])
                    })
                return data_list
            except aiohttp.ClientError as e:
                self.logger.exception(f"API request failed for {currency} from {start_date} to {end_date}")
                return None

    async def data_process_range(self, currency: str, start_date: str, end_date: str):
        """Process data from Awesome API for a range of dates."""
        days_qty = self.__get_days_quantity(start_date, end_date)

        data_bulk = await self.__fetch_historical_price(currency, start_date, end_date, days_qty)

        await self.client.close_session()

        self.storage.save(data_bulk)
