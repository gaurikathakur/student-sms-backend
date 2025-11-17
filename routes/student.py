# backend/routes/student.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Student
import json

student_bp = Blueprint("student_bp", __name__)
# ------------------- LOGIN -------------------
@student_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    student = Student.query.filter_by(username=username).first()
    if not student or not check_password_hash(student.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({
        "student": {
            "id": student.id,
            "name": student.name,
            "department": student.department,
            "semester": student.semester,
            "role": student.role
        }
    })


# Register & login routes unchanged (keep your existing ones).
# Below is the enriched dashboard route:

@student_bp.route("/dashboard/<int:student_id>", methods=["GET"])
def dashboard(student_id):
    s = Student.query.get(student_id)
    if not s:
        return jsonify({"error":"not found"}), 404

    # Use parsed to_dict output
    stud = s.to_dict()

    # Build semester CGPA data (example or from DB if you want dynamic)
    semesters = [
        {"sem":1,"cgpa":6.8},
        {"sem":2,"cgpa":7.4},
        {"sem":3,"cgpa":7.9},
        {"sem":4,"cgpa":8.1},
        {"sem":5,"cgpa":8.3},
        {"sem":6,"cgpa":s.cgpa or 8.0}
    ]

    # If attendance_weekly is an object: e.g. {"Week1":90,"Week2":88}
    attendance_weekly = stud.get("attendance_weekly", {}) or {}
    # convert to list for chart: [{week:"Week1", val:90}, ...]
    weekly_chart = [{"week": k, "percent": float(v)} for k,v in attendance_weekly.items()] if isinstance(attendance_weekly, dict) else []

    # Build demo timetable if not provided
    timetable = stud.get("timetable") or [
        {"day":"Monday","time":"9:00-11:00","class":"DBMS","room":"A-203"},
        {"day":"Wednesday","time":"11:00-1:00","class":"Web Dev","room":"C-201"},
    ]

    response = {
        "student": stud,
        "semesters": semesters,
        "attendance": {
            "overall": stud.get("attendance_semester") or "N/A",
            "weekly": weekly_chart
        },
        "marks": [
            {"subject":"Math","score":85},
            {"subject":"Data Structures","score":78}
        ],
        "seminars": [
            {"title":"AI Workshop","date":"2025-11-12"},
            {"title":"Cloud Computing Seminar","date":"2025-12-03"}
        ],
        "upcoming_holidays": [
            "2025-11-05 (Diwali)",
            "2025-12-25 (Christmas)"
        ],
        "leave_requests": [
            {"id":1,"from":"2025-11-01","to":"2025-11-03","status":"Approved"}
        ],
        "timetable": timetable
    }

    return jsonify(response)
@student_bp.route("/all", methods=["GET"])
def get_all_students():
    students = Student.query.all()

    result = []

    for s in students:
        result.append({
            "id": s.id,
            "name": s.name,
            "username": s.username,
            "mobile": s.mobile,
            "role": s.role,
            "semester": s.semester,
            "department": s.department,
            "current_address": s.current_address,
            "hometown": s.hometown,
            "cgpa": s.cgpa,
            "certifications": s.certifications,
            "extracurricular": s.extracurricular,
            "languages_known": s.languages_known,
            "attendance": s.attendance,
            "marks": s.marks,
            "timetable": s.timetable,
        })

    return jsonify(result), 200


@student_bp.route("/all", methods=["GET"])
def get_all_students():
    students = Student.query.all()
    result = []

    for s in students:
        stud = s.to_dict()  # use your existing parser

        result.append({
            "id": stud["id"],
            "name": stud["name"],
            "username": stud["username"],
            "mobile": stud["mobile"],
            "role": stud["role"],
            "semester": stud["semester"],
            "department": stud["department"],
            "current_address": stud["current_address"],
            "hometown": stud["hometown"],
            "cgpa": stud["cgpa"],

            # JSON lists
            "certifications": stud["certifications"],
            "extracurricular": stud["extracurricular"],
            "languages_known": stud["languages_known"],
            "library_books": stud["library_books"],
            "timetable": stud["timetable"],

            # Attendance fields
            "attendance_weekly": stud["attendance_weekly"],
            "attendance_semester": stud["attendance_semester"],
        })

    return jsonify(result), 200


