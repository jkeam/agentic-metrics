from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from dashboard.db import get_db, get_traces
from sqlalchemy import select, func, distinct
from chartkick.flask import PieChart, LineChart, ColumnChart, BarChart, AreaChart, ScatterChart
from math import ceil
from dashboard.utils.loader import dynamically_load_charts

bp = Blueprint('spans', __name__, url_prefix="/spans")

@bp.route('/', methods=["GET"])
def index():
    span_name = current_app.config["SPAN_NAME"]
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 50, type=int)
    db = get_db()
    tables = get_traces()
    with db.begin() as conn:
        traces = conn.execute(
            select(tables.c.SpanId, tables.c.TraceId, tables.c.Timestamp)
            .where(tables.c.SpanName == span_name)
            .order_by(tables.c.Timestamp.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        ).fetchall()
        total = conn.execute(
            select(func.count(distinct(tables.c.SpanId)))
            .where(tables.c.SpanName == span_name)
        ).scalar()
        total_pages = ceil(total / page_size)
    return render_template('spans/index.html', traces=traces, page=page, page_size=page_size, total=total, total_pages=total_pages)

@bp.route('/<id>/metrics', methods=["GET"])
def metrics(id):
    db = get_db()
    table = get_traces()
    with db.begin() as conn:
        trace = conn.execute(
            select(table.c.SpanId, table.c.TraceId, table.c.Timestamp, table.c["Events.Attributes"])
            .where(table.c.SpanId == id)
        ).first()

        span = {"span_id": trace.SpanId, "trace_id": trace.TraceId, "timestamp": trace.Timestamp}
        attrs = trace._mapping['Events.Attributes']
        dynamic_charts = dynamically_load_charts(span, attrs)
    return render_template(
        'spans/metrics.html',
        id=id,
        dynamic_charts=dynamic_charts,
    )

@bp.route('/<id>', methods=["GET"])
def show(id):
    db = get_db()
    table = get_traces()
    with db.begin() as conn:
        trace = conn.execute(
            select(table.c.SpanId, table.c.TraceId, table.c.Timestamp, table.c["Events.Attributes"])
            .where(table.c.SpanId == id)
        ).first()
    return render_template('spans/show.html', id=id, attrs=trace._mapping['Events.Attributes'])

