from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from dashboard.db import get_db, get_traces
from sqlalchemy import select
from chartkick.flask import PieChart

bp = Blueprint('traces', __name__, url_prefix="/traces")

@bp.route('/', methods=["GET"])
def index():
    db = get_db()
    traces = get_traces()
    with db.begin() as conn:
        traces = conn.execute(
            select(traces.c.TraceId, traces.c.Timestamp, traces.c["Events.Attributes"])
            .where(traces.c.SpanName == "Agentic Metrics")
            .order_by(traces.c.Timestamp.desc())
            .limit(1000)
        ).fetchall()
    return render_template('traces/index.html', traces=traces)
