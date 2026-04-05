from flask import current_app, g
from sqlalchemy import create_engine, MetaData, Table

def init_app(app):
    app.teardown_appcontext(close_db)

def get_db():
    if 'db' not in g:
        host = current_app.config["DB_HOST"]
        port = current_app.config["DB_PORT"]
        user = current_app.config["DB_USER"]
        password = current_app.config["DB_PASSWORD"]
        g.db = create_engine(f"clickhousedb://{user}:{password}@{host}:{port}/openlit")
    return g.db

def get_traces():
    if 'traces' not in g:
        db = get_db()
        metadata = MetaData(schema="openlit")
        g.traces = Table("otel_traces", metadata, autoload_with=db)
    return g.traces

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.dispose()
