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
from app.storage.postgres_storage import PostgresStorage


def current_date() -> str:
    """Get the current date in ISO format."""
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')

# Pass current_date as a callable, not as `current_date()`
@click.command()
@click.option('--currency', required=True, help='currency to get historical price for')
@click.option('--start_date', required=True, help='Start date in format YYYY-MM-DD')
@click.option('--end_date', required=True, help='End date in format YYYY-MM-DD')
@click.option('--save_mode', required=False, default='csv', help='postgres or csv options for save data')
@click.option('--concurrency_limit', required=False, default=5, type=int,
              help='Limit concurrency for requests')
async def app_main(currency, start_date, end_date, save_mode, concurrency_limit):
    """
    This function serves as the entry point for the CLI application that retrieves
    historical price data for a specified currency and date, then stores
    the fetched data into a specified storage location.
    """
    logger = logging.getLogger(__name__)
    logger.info("App Started")

    required_envs = {
        "API_CLIENT_NAME": os.getenv("API_CLIENT_NAME"),
        "STORAGE_PATH": os.getenv("STORAGE_PATH"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASS": os.getenv("DB_PASS"),
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_NAME": os.getenv("DB_NAME")
    }

    missing_envs = [key for key, value in required_envs.items() if not value]
    if missing_envs:
        logger.error(f"Missing environment variables: {', '.join(missing_envs)}. Exiting")
        sys.exit(1)

    database_url = (f"postgresql://{required_envs["DB_USER"]}:{required_envs["DB_PASS"]}@{required_envs["DB_HOST"]}"
                    f":{required_envs["DB_PORT"]}/{required_envs["DB_NAME"]}")
    logger.debug(f"Database URL: {database_url}")

    data_path = Path(required_envs["STORAGE_PATH"])
    data_path.mkdir(parents=True, exist_ok=True)
    csv_path = f"{data_path}/currency_data_{currency}_{current_date()}.csv"

    try:
        client = ClientFactory.get_client(api_name=required_envs["API_CLIENT_NAME"])
    except ValueError:
        logger.exception(f"Failed to initialize client")
        sys.exit(1)

    if save_mode not in ['csv', 'postgres']:
        logger.error(f"Unsupported save mode: {save_mode}")
        raise RuntimeError(f"Unsupported save mode: {save_mode}")
    else:
        storage = CSVStorage(csv_path) if save_mode == 'csv' else PostgresStorage(database_url)
    data_processor = DataProcessorResource(client=client, storage=storage, concurrency_limit=concurrency_limit)

    logger.info(f"Processing data for {currency} from {start_date} to {end_date}")
    await data_processor.data_process_range(currency, start_date, end_date)

    logger.info("App Finished")


if __name__ == "__main__":
    # global logging configuration
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()]  # Logs se envían a la consola
                        )
    app_main()
