# backend/seed_data.py
import os, sys, json
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app import create_app
from models import db, Student
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    admins = [
        {"name":"Gaurika Thakur","username":"gaurika","password":"admin123","role":"admin","department":"CS","semester":8},
        {"name":"Shankar Gaurek","username":"shankar","password":"admin123","role":"admin","department":"IT","semester":8}
    ]
    students = [
        {
            "name":"Aarav Sharma","username":"aarav","password":"student123","role":"student",
            "department":"CS-AI","semester":6,"cgpa":8.7,
            "attendance_weekly": json.dumps({"Week1":90,"Week2":92,"Week3":88,"Week4":91}),
            "attendance_semester":"91%",
            "library_books": json.dumps(["Data Science 101","Python Crash Course"]),
            "extracurricular": json.dumps(["Football","Drama Club"]),
            "certifications": json.dumps(["AI Basics","ML Nanodegree"]),
            "fees_status":"Paid",
            "timetable": json.dumps([{"day":"Monday","time":"9:00-11:00","class":"DBMS","room":"A-203"}]),
            "languages_known": json.dumps(["English","Hindi"])
        },
        {
            "name":"Kavya Singh","username":"kavya","password":"student123","role":"student",
            "department":"CS-DS","semester":5,"cgpa":8.3,
            "attendance_weekly": json.dumps({"Week1":88,"Week2":89,"Week3":87,"Week4":90}),
            "attendance_semester":"88%",
            "library_books": json.dumps(["Statistics for Data Science"]),
            "extracurricular": json.dumps(["Coding Club","Debate"]),
            "certifications": json.dumps(["Data Analysis Certificate"]),
            "fees_status":"Pending",
            "timetable": json.dumps([{"day":"Tuesday","time":"10:00-12:00","class":"Statistics","room":"B-101"}]),
            "languages_known": json.dumps(["English","Sanskrit"])
        },
        {
            "name":"Rahul Verma","username":"rahul","password":"student123","role":"student",
            "department":"CS-Cyber","semester":4,"cgpa":7.9,
            "attendance_weekly": json.dumps({"Week1":84,"Week2":86,"Week3":83,"Week4":85}),
            "attendance_semester":"85%",
            "library_books": json.dumps(["Cybersecurity Essentials"]),
            "extracurricular": json.dumps(["Robotics Club"]),
            "certifications": json.dumps(["Intro to Networking"]),
            "fees_status":"Paid",
            "timetable": json.dumps([{"day":"Friday","time":"2:00-4:00","class":"Cybersecurity","room":"D-302"}]),
            "languages_known": json.dumps(["English","Hindi","German"])
        }
    ]

    for a in admins:
        s = Student(
            name=a["name"],
            username=a["username"],
            password=generate_password_hash(a["password"]),
            role=a["role"],
            department=a["department"],
            semester=a["semester"],
            cgpa=a.get("cgpa",0.0)
        )
        db.session.add(s)

    for st in students:
        s = Student(
            name=st["name"],
            username=st["username"],
            password=generate_password_hash(st["password"]),
            role=st["role"],
            department=st["department"],
            semester=st["semester"],
            cgpa=st.get("cgpa",0.0),
            attendance_weekly=st.get("attendance_weekly"),
            attendance_semester=st.get("attendance_semester"),
            library_books=st.get("library_books"),
            extracurricular=st.get("extracurricular"),
            certifications=st.get("certifications"),
            fees_status=st.get("fees_status"),
            timetable=st.get("timetable"),
            languages_known=st.get("languages_known")
        )
        db.session.add(s)

    db.session.commit()
    print("Seed complete.")
