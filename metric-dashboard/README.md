# Dashboard

Assuming you have already run the instructions found in `../metric-generator`.

## Environment

```shell
# this project gets created from the ../metric-generator project
oc project openlit
# expose db
oc apply -f ./openshift/db-route.yaml
```

## Setup

```shell
uv python pin 3.12
uv sync
```

Create an `.env` file with the following (replace with real values):

```shell
DB_HOST=your-clickhouse-db.com
DB_PORT=8123
DB_USER=default
DB_PASSWORD=OPENLIT
DYNAMIC_CHART_PATH="" # empty string turns off dynamic chart functionality
```

## Run

```shell
uv run --env-file .env flask --app dashboard run
```

## Building

```shell
cd ./metric-dashboard
# replace with your own repo
podman build -t quay.io/jkeam/metric-dashboard -f ./Containerfile .
# test by running it
# podman run --rm --env-file .env -p 8000:8000 -t quay.io/jkeam/metric-dashboard
```
