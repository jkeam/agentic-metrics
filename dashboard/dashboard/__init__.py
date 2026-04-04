from os import makedirs, getenv

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.config["DB_HOST"] = getenv("DB_HOST", "openlit-db.openlit.svc.cluster.local")
    app.config["DB_PORT"] = int(getenv("DB_PORT", "8123"))
    app.config["DB_USER"] = getenv("DB_USER", "default")
    app.config["DB_PASSWORD"] = getenv("DB_PASSWORD", "OPENLIT")

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

    @app.route('/healthz')
    def healthz():
        return 'healthy'

    from . import dashboard
    app.register_blueprint(dashboard.bp)

    return app
