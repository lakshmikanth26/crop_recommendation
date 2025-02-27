from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import routes from routes.py
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
