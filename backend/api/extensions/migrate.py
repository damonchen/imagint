from flask_migrate import Migrate


migrate = Migrate()


def init_app(app):
    from .database import db

    migrate.init_app(app, db)
