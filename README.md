## Introduction
Implemented SSRF vulnerability in LLM integrated web based on a simple financial app.

## Installation

### Prerequisites
* [Docker](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Steps
1. Clone the Repository
```
git clone https://github.com/WHS-LLM-Integrated-Webhacking/Broken-finance
cd Broken-finance
```
2. Setting environment variables within Docker Compose
```
services:
  api:
    build: 
      context: .
      dockerfile: DockerfileAPI
    volumes:
      - ./api:/app
    ports:
      - "5000:5000"
    links:
      - db
    environment:
      - MYSQL_HOST=db
      - MYSQL_DB=finance
      - FLASK_APP=app.py
      - FLASK_RUN_HOST=0.0.0.0
      - GOOGLE_API_KEY=YOURAPIKEY
      - OPENAI_API_KEY=YOURAPIKEY
      - GOOGLE_CSE=YOURCSE
    depends_on:
      - db
...
```


3. Build
```
docker-compose up --build
```
4. Access
Open a browser and navigate to http://127.0.0.1:8000
