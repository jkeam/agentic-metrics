# Dashboard

Assuming you have already run the instructions found in `../metric-generator`.

## Environment

```shell
oc project openlit
oc apply -f ./openshift/db-route.yaml
```

## Setup

```shell
uv python pin 3.11
uv sync
```

Create an `.env` file with the following (replace with real values):

```shell
DB_HOST=your-clickhouse-db.com
DB_PORT=8123
DB_USER=default
DB_PASSWORD=OPENLIT
```

## Run

```shell
uv run --env-file .env flask --app dashboard run
```
