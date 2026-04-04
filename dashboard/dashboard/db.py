from sqlalchemy import create_engine
from flask import current_app, g

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


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.dispose()
