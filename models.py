# backend/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashed
    role = db.Column(db.String(20), default="student")  # 'student' or 'admin'
    department = db.Column(db.String(80), default="CS")
    semester = db.Column(db.Integer, default=1)
    cgpa = db.Column(db.Float, default=0.0)
    hometown = db.Column(db.String(200), nullable=True)
    current_address = db.Column(db.String(300), nullable=True)
    dob = db.Column(db.String(30), nullable=True)
    mobile = db.Column(db.String(50), nullable=True)
    secret_question = db.Column(db.String(255), nullable=True)
    secret_answer = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # New fields stored as JSON strings (for simplicity)
    attendance_weekly = db.Column(db.Text, nullable=True)       # JSON: {"Week1":90,"Week2":88,...}
    attendance_semester = db.Column(db.String(50), nullable=True) # e.g. "92%"
    library_books = db.Column(db.Text, nullable=True)           # comma-separated or JSON list
    extracurricular = db.Column(db.Text, nullable=True)        # comma-separated
    certifications = db.Column(db.Text, nullable=True)         # comma-separated
    fees_status = db.Column(db.String(50), nullable=True)      # "Paid" / "Pending"
    timetable = db.Column(db.Text, nullable=True)              # JSON list of schedule objects
    languages_known = db.Column(db.Text, nullable=True)        # comma-separated

    def to_dict(self):
        # helper to safely parse JSON fields
        def parse_json_field(v, default):
            if not v:
                return default
            try:
                return json.loads(v)
            except Exception:
                # if plain comma-separated string, split:
                if isinstance(v, str) and "," in v:
                    return [s.strip() for s in v.split(",") if s.strip()]
                return v

        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "role": self.role,
            "department": self.department,
            "semester": self.semester,
            "cgpa": self.cgpa,
            "hometown": self.hometown,
            "current_address": self.current_address,
            "dob": self.dob,
            "mobile": self.mobile,
            "attendance_weekly": parse_json_field(self.attendance_weekly, {}),
            "attendance_semester": self.attendance_semester,
            "library_books": parse_json_field(self.library_books, []),
            "extracurricular": parse_json_field(self.extracurricular, []),
            "certifications": parse_json_field(self.certifications, []),
            "fees_status": self.fees_status,
            "timetable": parse_json_field(self.timetable, []),
            "languages_known": parse_json_field(self.languages_known, []),
        }
