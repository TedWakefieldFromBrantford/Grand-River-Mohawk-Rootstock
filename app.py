# app.py
import os
from flask import Flask
from config import Config
from models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure instance folder exists for SQLite
    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register the routes from routes.py
    from routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
