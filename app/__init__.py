from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    login.login_view = 'login'

    with app.app_context():
        from app.blueprints.api import bp as api
        app.register_blueprint(api)

        from app.blueprints.auth import bp as auth
        app.register_blueprint(auth)

        from app.blueprints.main import bp as main
        app.register_blueprint(main)

        from app.blueprints.movies import bp as movie
        app.register_blueprint(movie)

        from app.blueprints.ratings import bp as ratings
        app.register_blueprint(ratings)

        from app.blueprints.watchlist import bp as watchlist
        app.register_blueprint(watchlist)

    return app