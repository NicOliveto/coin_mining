# Historical Currency Price

This project retrieves historical price data for a specific currency on 
a given using Awesome API, processes the data, and stores it either in a PostgreSQL database or as CSV file.

---

### Features

- Fetch historial currency price data using the Awesome API
- Preloaded SQL database schema and table.
- Customizable concurrency for API requests.
- Store data in PostgreSQL or CSV file formats¿.

---

### Requirements

#### Prerequisites:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

#### Python Packages

The application requires Python 3.12.8 and uses some of the following Python libraries, 

- `asyncclick`: Asynchronous version of Click for CLI development.
- `aiohttp`: : Asynchronous HTTP client for data fetching.
- `SQLAlchemy`: Database ORM for handling PostgreSQL operations.

For more information about the other libraries listed, see `requirements.txt`

---

### Setting up the Project

#### 1. Clone the Repository:

```bash
git clone <repository_url>
cd <repository_name>
```

#### 2. Configure Environment Variables

Create `.env` file located in `config/` with the required environment variables

```dotenv
API_CLIENT_NAME=awesomeapi
STORAGE_PATH=/apiapp/data/
DB_USER=challengemeli_usr
DB_PASS=password
DB_HOST=postgres
DB_PORT=5432
DB_NAME=challengemeli_db
```

Create `.env` file located in `db/` with the required environment variables

```dotenv
POSTGRES_USER=challengemeli_usr
POSTGRES_PASSWORD=password
POSTGRES_DB=challengemeli_db
```

#### 3. Docker Setup

Build and run the services using docker-compose-yaml. This docker-compose works for both services (application & 
postgres database) and includes all the requirements needed it:

##### Build and Start the containers:

```shell
docker-compose up --build -d
```

This will:
- Build the `postgres` service and initialize the database using the `currency_data.sql` script.
- Launch a Python container with the currency processing application.

---

### Preloaded Database (`currency_data.sql`)

The PostgreSQL service is initialized with the `currency_data.sql` script, which creates the following schema and tables:

### Schema and Tables

1. **Schema: `relational_tb`**
2. **Table: `test.currency_data`**
   - Primary key: `(base_currency_id, target_currency_id, date_time)`
   - Stores prices for currencies with the following columns:
     - `base_currency_id`: ID of the base currency (e.g., `USD`).
     - `target_currency_id`: ID of the target currency (e.g., `BRL`)
     - `date_time`: Timestamp of the final price of the date.
     - `purchase_amt`: Value of the purchase amount.
     - `sale_amt`: Value of the sale amount.
     - 
---

### Running the Application

You can execute the CLI application directly from the `app` container. For example:

```shell
docker-compose exec app python coin_mining.py --currency <currency_id> --start_date <YYYY-MM_DD> --end_date <YYYY-MM-DD> --save_mode <SAVE_MODE>
```

#### Command-Line Options
- `--currency`: The currency ID to fetch (e.g., `USD-BRL` or `EUR-BRL` or `BTC-BRL`).
- `--start_date`: Start date in `YYYY-MM-DD` format.
- `--end_date`: End date in `YYYY-MM-DD` format.
- `--save_mode`: Choose either `postgres` or `CSV` for storage.
- `--concurrency_limit`: Optional, default is `5`. Limit for concurrent API requests.

---

### Stopping Application Service

To stop the containers, run:

```shell
docker-compose down
```

(Optional) If you want to remove images and volumes, run:
```shell
docker-compose down --rmi all -v --remove-orphans
```

---

## Docker Details

### `docker-compose.yaml`

Defines two services:
1. **Postgres Service**:
   - Uses a custom Dockerfile located in `db/`.
   - Initializes the database with the `db/data/currency_data.sql` script.
   - Stores persistent data using a Docker volume (`pg_data`).

2. **Python App Service**:
   - Uses a custom Dockerfile located in `config/`.
   - Mounts the `data` directory for saving CSV outputs.
   - Depends on the `postgres` service to ensure database availability.

---

## Volumes

The project use the following volumes:

- `pg_data`: Ensures PostgreSQL database data is persisted across runs.
- `data`: Maps application-generated CSV files to a host directory.

---

## Folder Structure

- `/app`: Contains the Python libraries for `coin_mining.py`.
- `/db`: Contains the PostgreSQL database configuration, dockerfile, `.env` and initial script.
- `/config`: includes configuration files like `.env` and Dockerfile for `coin_mining.py`
