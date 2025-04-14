from abc import ABC, abstractmethod
import aiohttp

class ApiClient(ABC):
    def __init__(self):
        self.session = aiohttp.ClientSession()

    @abstractmethod
    def get_base_url(self):
        pass

    @abstractmethod
    def get_historical_price(self, currency: str, start_date: str, end_date: str, days: int):
        pass

    async def fetch_data(self, request_data: dict):
        try:
            async with self.session.get(request_data["url"], headers=request_data["headers"]) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error fetching data from {request_data['url']}: {e}")
            return None

    async def close_session(self):
        await self.session.close()
