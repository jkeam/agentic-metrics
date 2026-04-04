from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from dashboard.db import get_db
from sqlalchemy import MetaData, Table, select

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    db = get_db()
    metadata = MetaData(schema="openlit")
    traces = Table("otel_traces", metadata, autoload_with=db)
    with db.begin() as conn:
        traces = conn.execute(
            select(traces.c.TraceId, traces.c.Timestamp, traces.c["Events.Attributes"])
            .where(traces.c.SpanName == "Agentic Metrics")
            .order_by(traces.c.Timestamp.asc())
            .limit(10)
        ).fetchall()
    return render_template('dashboard/index.html', traces=traces)
