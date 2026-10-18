from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import ApplicationForm
from app.models import STATUSES, Application

bp = Blueprint("applications", __name__)

SORTS = {
    "newest": Application.date_applied.desc(),
    "oldest": Application.date_applied.asc(),
    "company": Application.company.asc(),
}


def get_owned(app_id):
    """Fetch an application only if it belongs to the logged-in user, else 404."""
    return db.first_or_404(db.select(Application).filter_by(id=app_id, user_id=current_user.id))


@bp.get("/")
@login_required
def list_():
    status = request.args.get("status", "")
    q = request.args.get("q", "").strip()
    sort = request.args.get("sort", "newest")
    stmt = db.select(Application).filter_by(user_id=current_user.id)
    if status in STATUSES:
        stmt = stmt.filter_by(status=status)
    if q:
        stmt = stmt.where(Application.company.ilike(f"%{q}%"))
    stmt = stmt.order_by(SORTS.get(sort, SORTS["newest"]), Application.id.desc())
    page = db.paginate(stmt, page=request.args.get("page", 1, type=int), per_page=10, error_out=False)
    args = {k: v for k, v in request.args.items() if k != "page"}
    return render_template("applications/list.html", page=page, args=args,
                           statuses=STATUSES, status=status, q=q, sort=sort)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = ApplicationForm()
    if form.validate_on_submit():
        app_ = Application(user_id=current_user.id)
        form.populate_obj(app_)
        db.session.add(app_)
        db.session.commit()
        flash("Application added.", "ok")
        return redirect(url_for("applications.list_"))
    return render_template("applications/form.html", form=form, title="Add application")


@bp.route("/<int:app_id>/edit", methods=["GET", "POST"])
@login_required
def edit(app_id):
    app_ = get_owned(app_id)
    form = ApplicationForm(obj=app_)
    if form.validate_on_submit():
        form.populate_obj(app_)
        db.session.commit()
        flash("Changes saved.", "ok")
        return redirect(url_for("applications.list_"))
    return render_template("applications/form.html", form=form, title=f"Edit {app_.company}")


@bp.post("/<int:app_id>/delete")
@login_required
def delete(app_id):
    db.session.delete(get_owned(app_id))
    db.session.commit()
    flash("Application deleted.", "ok")
    return redirect(url_for("applications.list_"))
