# Historical Currency Price

This project retrieves historical price data for a specific currency on 
a given using Awesome API, processes the data, and stores in a CSV file.

---

### Features

- Fetch historial cryptocurrency price data using the Awesome API
- Customizable concurrency for API requests.
- Store data in a CSV file formats¿.

---

### Requirements

#### Prerequisites:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

#### Python Packages

The application requires Python 3.12.8 and uses some of the following Python libraries, 

- `asyncclick`: Asynchronous version of Click for CLI development.
- `aiohttp`: : Asynchronous HTTP client for data fetching.

For more information about the other libraries listed, see `requirements.txt`

---

### Setting up the Project

#### 1. Clone the Repository:

```bash
git clone <repository_url>
cd <repository_name>
```

#### 2. Configure Environment Variables

Create `.env` file located in `app/` with the required environment variables

```dotenv
API_CLIENT_NAME=awesomeapi
STORAGE_PATH=/apiapp/data/
```

#### 3. Docker Setup

Build and run the service using docker-compose-yaml. This docker-compose works for application and includes all the requirements needed it:

##### Build and Start the containers:

```shell
docker-compose up --build -d
```

This will:
- Launch a Python container with the currency processing application.

---

### Running the Application

You can execute the CLI application directly from the `app` container. For example:

```shell
docker-compose exec app python coin_mining.py --currency <currency_id> --start_date <YYYY-MM_DD> --end_date <YYYY-MM-DD>
```

#### Command-Line Options
- `--currency`: The currency ID to fetch (e.g., `USD-BRL` or `EUR-BRL` or `BTC-BRL`).
- `--start_date`: Start date in `YYYY-MM-DD` format.
- `--end_date`: End date in `YYYY-MM-DD` format.
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

**Python App Service**:
   - Uses a custom Dockerfile located in main root.
   - Mounts the `data` directory for saving CSV outputs.

---

## Volumes

The project use the following volumes:

- `data`: Maps application-generated JSON files to a host directory.

---

## Folder Structure

- `/app`: Contains the libraries of python application.
- `main root`: Contains configurations files, dockerfile and dockercompose.
