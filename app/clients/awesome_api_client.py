from datetime import datetime
from .api_client import ApiClient
from app.builders.api_request_builder import ApiRequestBuilder

class AwesomeApiClient(ApiClient):
    def get_base_url(self):
        return "https://economia.awesomeapi.com.br/json/daily/"

    async def get_historical_price(self, currency: str, start_date: str, end_date: str, days: int = 1):
        format_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y%m%d")
        format_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y%m%d")
        endpoint = "{moeda}/{numero_dias}/"
        path_params = {"moeda": currency, "numero_dias": days}
        query_params = {"start_date": format_start_date, "end_date": format_end_date}

        url_builder = ApiRequestBuilder().set_base_url(self.get_base_url()).set_endpoint(endpoint)

        if path_params:
            for key, value in path_params.items():
                url_builder.set_path_param(key, value)

        if query_params:
            for key, value in query_params.items():
                url_builder.add_query_param(key, value)

        request_data = url_builder.build()

        response = await self.fetch_data(request_data)

        if response is None:
            raise RuntimeError("Failed to retrieve historical price data from AwesomeAPI.")
        if "error" in response:
            raise ValueError(f"Error from Awesome API: {response['error']}")

        return response