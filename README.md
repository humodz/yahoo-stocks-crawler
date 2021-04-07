# yahoo-stocks-crawler

### Endpoints

- Swagger docs: `http://localhost:8000/docs`
- ReDoc docs: `http://localhost:8000/redoc`
- Stocks: `http://localhost:8000/stocks?region=Brazil`

### Commands

##### Install dependencies
```sh 
poetry install
```
##### Run server (will start Redis)
```sh
poetry run ./scripts/start.sh
```
##### Run tests (will start Redis)
```sh 
poetry run ./scripts/test.sh
```
##### Run server using Docker
```sh
./scripts/docker-compose.sh up --build
```

### Requirements

- Python >=3.7
- Poetry
    - https://python-poetry.org/
- Docker and Docker Compose
- Chrome or Chromium
- WebDriver
    - For Chrome
        - `sudo apt install chromedriver`; or
        - Manual download
            - https://sites.google.com/a/chromium.org/chromedriver/downloads
    - For Chromium
        - Ubuntu/Mint: `sudo apt install chromium-chromedriver`; or
        - Debian: `sudo apt install chromium-driver`
