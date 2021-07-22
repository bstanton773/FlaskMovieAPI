from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app)
    login.init_app(app)

    login.login_view = 'login'

    with app.app_context():
        from app import routes, models

        from app.blueprints.auth import bp as auth
        app.register_blueprint(auth)

    return app