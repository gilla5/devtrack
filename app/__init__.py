import os

from flask import Flask

from app.extensions import csrf, db, login_manager


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_object("config.Config")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(app.instance_path, "devtrack.db")
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.applications.routes import bp as applications_bp
    from app.auth.routes import bp as auth_bp
    from app.dashboard.routes import bp as dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(applications_bp, url_prefix="/applications")
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        db.create_all()  # swap for Flask-Migrate once the schema starts changing
    return app
