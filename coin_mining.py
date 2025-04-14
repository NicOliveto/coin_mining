import sys
import logging
import os
import asyncio
import asyncclick as click
from datetime import datetime, timezone, timedelta
from pathlib import Path
from app.resources.data_processor_resource import DataProcessorResource
from app.providers.client_factory import ClientFactory
from app.storage.csv_storage import CSVStorage


def current_date() -> str:
    """Get the current date in ISO format."""
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')

# Pass current_date as a callable, not as `current_date()`
@click.command()
@click.option('--currency', required=True, help='currency to get historical price for')
@click.option('--start_date', required=True, help='Start date in format YYYY-MM-DD')
@click.option('--end_date', required=True, help='End date in format YYYY-MM-DD')
@click.option('--concurrency_limit', required=False, default=5, type=int,
              help='Limit concurrency for requests')
async def app_main(currency, start_date, end_date, concurrency_limit):
    """
    This function serves as the entry point for the CLI application that retrieves
    historical price data for a specified cryptocurrency and date, then stores
    the fetched data into a specified storage location.
    """
    logger = logging.getLogger(__name__)
    logger.info("App Started")

    required_envs = {
        "API_CLIENT_NAME": os.getenv("API_CLIENT_NAME"),
        "STORAGE_PATH": os.getenv("STORAGE_PATH"),
    }

    missing_envs = [key for key, value in required_envs.items() if not value]
    if missing_envs:
        logger.error(f"Missing environment variables: {', '.join(missing_envs)}. Exiting")
        sys.exit(1)

    data_path = Path(required_envs["STORAGE_PATH"])
    data_path.mkdir(parents=True, exist_ok=True)
    csv_path = f"{data_path}/currency_data_{currency}_{current_date()}.csv"

    try:
        client = ClientFactory.get_client(api_name=required_envs["API_CLIENT_NAME"])
    except ValueError:
        logger.exception(f"Failed to initialize client")
        sys.exit(1)

    storage = CSVStorage(csv_path)
    data_processor = DataProcessorResource(client=client, storage=storage, concurrency_limit=concurrency_limit)

    logger.info(f"Processing data for {currency} from {start_date} to {end_date}")
    await data_processor.data_process_range(currency, start_date, end_date)

    logger.info("App Finished")


if __name__ == "__main__":
    # global logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()]  # Logs se envían a la consola
                        )
    asyncio.run(app_main(), debug=True)
