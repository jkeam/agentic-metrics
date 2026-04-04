# Metric Generator
App to demonstrate create agentic metrics.

## Environment

```shell
# create deployment
oc new-project openlit
oc adm policy add-scc-to-user anyuid -z default -n openlit
oc apply -f ./openshift/helm-repo.yaml
# use OpenShift Web Console to create helm deployment

# create routes
oc apply -f ./openshift/openlit-route.yaml
oc apply -f ./openshift/openlit-otel-route.yaml

# troubleshooting, if you see missing `NEXTAUTH_SECRET`,
#   then connect to the pod and delete `/app/client/data/.nextauth_secret`
```

## Setup

```shell
uv python pin 3.11
uv sync
```

Create an `.env` file with the following (replace with real values):

```shell
CREWAI_TRACING_ENABLED=false
OTEL_EXPORTER_OTLP_ENDPOINT="http://your-otel-endpoint.com"
LLM_API_KEY="sk-your-key-here"
LLM_BASE_URL="https://litellm-prod.apps.maas.redhatworkshops.io/v1/"
LLM_MODEL_NAME="model-name"
```

## Run

```shell
uv run --env-file .env ./main.py
```

## Lint

```shell
uv black ./main.py
```
