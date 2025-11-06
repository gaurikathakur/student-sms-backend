from app import app, db, Student

with app.app_context():
    db.create_all()

    # Admins
    gaurika = Student(name="Gaurika", department="CS", semester=8, username="gaurika", password="admin123", role="admin")
    shankar = Student(name="Shankar", department="CS", semester=8, username="shankar", password="admin123", role="admin")

    # Students
    kavya = Student(name="Kavya", department="CS", semester=3, username="kavya", password="student123", role="student")
    arihant = Student(name="Arihant", department="CS AI", semester=2, username="arihant", password="student123", role="student")

    db.session.add_all([gaurika, shankar, kavya, arihant])
    db.session.commit()
    print("✅ Database seeded successfully!")
