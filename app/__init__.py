from flask import Flask # type: ignore
from .config import Config
from .models import db, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from .routes import main
        app.register_blueprint(main)

        # Create tables if they don't exist
        db.create_all()

    return app
