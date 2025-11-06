import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, Student


def seed():
    with app.app_context():
        db.create_all()
        admins = [
            Student(name="Gaurika", department="CS", semester=1, username="gaurika", password="admin123", role="admin"),
            Student(name="Shankar", department="CS", semester=1, username="shankar", password="admin123", role="admin")
        ]
        db.session.add_all(admins)
        db.session.commit()
        print("✅ Admins seeded successfully!")

if __name__ == "__main__":
    seed()
