from clickhouse_connect import get_client
from os import getenv
from sqlalchemy import create_engine, MetaData, Table, select


def main():
    host = getenv("DB_HOST", "openlit-db.openlit.svc.cluster.local")
    port = int(getenv("DB_PORT", "8123"))
    user = getenv("DB_USER", "default")
    password = getenv("DB_PASSWORD", "OPENLIT")

    engine = create_engine(f"clickhousedb://{user}:{password}@{host}:{port}/openlit")
    metadata = MetaData(schema="openlit")
    traces = Table("otel_traces", metadata, autoload_with=engine)
    with engine.begin() as conn:
        rows = conn.execute(
            select(traces.c.TraceId, traces.c.Timestamp, traces.c["Events.Attributes"])
            .where(traces.c.SpanName == "Agentic Metrics")
            .order_by(traces.c.Timestamp.asc())
            .limit(10)
        ).fetchall()
        print(rows)


if __name__ == "__main__":
    main()
