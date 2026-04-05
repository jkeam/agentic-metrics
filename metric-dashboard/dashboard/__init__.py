from os import makedirs, getenv
from chartkick.flask import chartkick_blueprint
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DB_HOST = getenv("DB_HOST", "openlit-db.openlit.svc.cluster.local"),
        DB_PORT = int(getenv("DB_PORT", "8123")),
        DB_USER = getenv("DB_USER", "default"),
        DB_PASSWORD = getenv("DB_PASSWORD", "OPENLIT"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)

    app.register_blueprint(chartkick_blueprint)
    from . import home
    app.register_blueprint(home.bp)
    from . import traces
    app.register_blueprint(traces.bp)

    return app
