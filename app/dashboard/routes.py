from datetime import date, timedelta

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.extensions import db
from app.models import STATUSES, Application

bp = Blueprint("dashboard", __name__)


def pct(n, d):
    return round(100 * n / d) if d else 0  # safe with zero applications


@bp.get("/")
@login_required
def index():
    apps = db.session.scalars(
        db.select(Application).filter_by(user_id=current_user.id)
        .order_by(Application.date_applied.desc(), Application.id.desc())
    ).all()
    counts = {s: sum(a.status == s for a in apps) for s in STATUSES}
    applied = len(apps) - counts["Wishlist"]
    interviews = counts["Interviewing"] + counts["Offer"]
    today = date.today()
    soon = today + timedelta(days=7)
    followups = sorted(
        (a for a in apps if a.next_followup and a.next_followup <= soon and a.status not in ("Offer", "Rejected")),
        key=lambda a: a.next_followup,
    )
    stats = {
        "total": len(apps), "applied": applied, "interviews": interviews, "offers": counts["Offer"],
        "interview_rate": pct(interviews, applied), "offer_rate": pct(counts["Offer"], interviews),
    }
    board = {s: [a for a in apps if a.status == s] for s in STATUSES}
    return render_template("dashboard/index.html", stats=stats, board=board, followups=followups, today=today)
