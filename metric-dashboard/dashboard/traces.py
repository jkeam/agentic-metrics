from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from dashboard.db import get_db, get_traces
from sqlalchemy import select, func, distinct
from chartkick.flask import PieChart
from math import ceil

bp = Blueprint('traces', __name__, url_prefix="/traces")

@bp.route('/', methods=["GET"])
def index():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 50, type=int)
    db = get_db()
    traces = get_traces()
    with db.begin() as conn:
        traces_result = conn.execute(
            select(traces.c.SpanId, traces.c["Events.Attributes"])
            .where(traces.c.SpanName == "Agentic Metrics")
            .order_by(traces.c.Timestamp.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        ).fetchall()
        total = conn.execute(
            select(func.count(distinct(traces.c.SpanId)))
            .where(traces.c.SpanName == "Agentic Metrics")
        ).scalar()
        total_pages = ceil(total / page_size)
    return render_template('traces/index.html', traces=traces_result, page=page, page_size=page_size, total=total, total_pages=total_pages)

@bp.route('/<span_id>/<trace_uuid>', methods=["GET"])
def show(span_id, trace_uuid):
    db = get_db()
    table = get_traces()
    with db.begin() as conn:
        trace = conn.execute(
            select(table.c.SpanId, table.c.TraceId, table.c.Timestamp, table.c["Events.Attributes"])
            .where(table.c.SpanId == span_id)
        ).first()
        attrs = trace._mapping['Events.Attributes']
        trace = next((a for a in attrs if a["uuid"] == trace_uuid), None)
    return render_template('traces/show.html', span_id=span_id, trace=trace)
