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
    db = get_db()
    table = get_traces()
    with db.begin() as conn:
        traces = conn.execute(
            select(table.c.SpanId, table.c.TraceId, table.c.Timestamp, table.c["Events.Attributes"])
            .where(table.c.SpanName == "Agentic Metrics")
            .order_by(table.c.Timestamp.desc())
            .limit(10)
        ).fetchall()
        chart_ltps = PieChart({'Blueberry': 44, 'Strawberry': 23})
        chart_dhplc = PieChart({'Blueberry': 44, 'Strawberry': 23})
        chart_df = PieChart({'Blueberry': 44, 'Strawberry': 23})
        chart_tcrr = PieChart({'Blueberry': 44, 'Strawberry': 23})
        chart_dlr = PieChart({'Blueberry': 44, 'Strawberry': 23})
        chart_tdr = PieChart({'Blueberry': 44, 'Strawberry': 23})
        chart_bfc = PieChart({'Blueberry': 44, 'Strawberry': 23})
    return render_template(
        'home/index.html',
        chart_ltps=chart_ltps,
        chart_dhplc=chart_dhplc,
        chart_df=chart_df,
        chart_tcrr=chart_tcrr,
        chart_dlr=chart_dlr,
        chart_tdr=chart_tdr,
        chart_bfc=chart_bfc,
    )
