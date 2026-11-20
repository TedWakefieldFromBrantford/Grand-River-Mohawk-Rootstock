import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db

def create_tables():
    app = create_app()
    with app.app_context():
        # This creates any tables that don't exist yet.
        # It will NOT drop or overwrite existing tables.
        db.create_all()
        print("Database tables created/verified successfully!")

if __name__ == "__main__":
    create_tables()
