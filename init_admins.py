from backend.models import User, db

def create_admins():
    admins = [
        {"username": "gaurika", "password": "Gaurika@123", "role": "Admin", "name": "Gaurika Shanker"},
        {"username": "shankar", "password": "Shankar@123", "role": "Admin", "name": "Shankar"}
    ]

    for admin in admins:
        if not User.query.filter_by(username=admin["username"]).first():
            db.session.add(User(**admin))
    db.session.commit()
    print("Admins created.")
