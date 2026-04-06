from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from dashboard.db import get_db, get_traces
from sqlalchemy import select, func, distinct
from chartkick.flask import PieChart
from math import ceil

bp = Blueprint('spans', __name__, url_prefix="/spans")

@bp.route('/', methods=["GET"])
def index():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 50, type=int)
    db = get_db()
    tables = get_traces()
    with db.begin() as conn:
        traces = conn.execute(
            select(tables.c.SpanId, tables.c.TraceId, tables.c.Timestamp)
            .where(tables.c.SpanName == "Agentic Metrics")
            .order_by(tables.c.Timestamp.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        ).fetchall()
        total = conn.execute(
            select(func.count(distinct(tables.c.SpanId)))
            .where(tables.c.SpanName == "Agentic Metrics")
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
        attrs = trace._mapping['Events.Attributes']
        # lead time per story
        chart_ltps = PieChart({'Blueberry': 44, 'Strawberry': 23})
        # lines of code
        chart_dhplc = PieChart({'Blueberry': 44, 'Strawberry': 23})
        # deployment freq
        chart_df = PieChart({'Blueberry': 44, 'Strawberry': 23})
        # test coverage recovery rate
        chart_tcrr = PieChart({'Blueberry': 44, 'Strawberry': 23})
        # defect leakage rate
        chart_dlr = PieChart({'Blueberry': 44, 'Strawberry': 23})
        # technical debt reduction
        chart_tdr = PieChart({'Blueberry': 44, 'Strawberry': 23})
        # behavior fidelity capture
        chart_bfc = PieChart({'Blueberry': 44, 'Strawberry': 23})
    return render_template(
        'spans/metrics.html',
        id=id,
        chart_ltps=chart_ltps,
        chart_dhplc=chart_dhplc,
        chart_df=chart_df,
        chart_tcrr=chart_tcrr,
        chart_dlr=chart_dlr,
        chart_tdr=chart_tdr,
        chart_bfc=chart_bfc,
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

