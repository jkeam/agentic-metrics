from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
)
from werkzeug.exceptions import abort
from dashboard.db import get_db, get_traces
from sqlalchemy import select
from chartkick.flask import PieChart

bp = Blueprint('home', __name__, url_prefix="/")

@bp.route('/healthz')
def healthz():
    return 'healthy'

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon/favicon.ico')

@bp.route('/site.webmanifest')
def manifest():
    return send_from_directory('static', 'favicon/site.webmanifest')

@bp.route('/web-app-manifest-192x192.png')
def webapp_manifest192():
    return send_from_directory('static', 'favicon/web-app-manifest-192x192.png')

@bp.route('/web-app-manifest-512x512.png')
def webapp_manifest512():
    return send_from_directory('static', 'favicon/web-app-manifest-512x512.png')

@bp.route('/', methods=["GET"])
def index():
    return render_template('home/index.html')
