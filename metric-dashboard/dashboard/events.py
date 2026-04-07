from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from dashboard.db import get_db, get_traces
from sqlalchemy import select, func, distinct
from chartkick.flask import PieChart
from math import ceil

bp = Blueprint('events', __name__, url_prefix="/events")

@bp.route('/', methods=["GET"])
def index():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 50, type=int)
    db = get_db()
    table = get_traces()
    with db.begin() as conn:
        span_name = current_app.config["SPAN_NAME"]
        traces = conn.execute(
            select(table.c.SpanId, table.c["Events.Attributes"])
            .where(table.c.SpanName == span_name)
            .order_by(table.c.Timestamp.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        ).fetchall()
        total = conn.execute(
            select(func.count(distinct(table.c.SpanId)))
            .where(table.c.SpanName == span_name)
        ).scalar()
        total_pages = ceil(total / page_size)
    return render_template('events/index.html', traces=traces, page=page, page_size=page_size, total=total, total_pages=total_pages)

@bp.route('/<span_id>/<event_uuid>', methods=["GET"])
def show(span_id, event_uuid):
    db = get_db()
    table = get_traces()
    with db.begin() as conn:
        trace = conn.execute(
            select(table.c.SpanId, table.c.TraceId, table.c.Timestamp, table.c["Events.Attributes"])
            .where(table.c.SpanId == span_id)
        ).first()
        attrs = trace._mapping['Events.Attributes']
        event = next((a for a in attrs if a["uuid"] == event_uuid), None)
    return render_template('events/show.html', span_id=span_id, event=event)
