from flask import Blueprint, jsonify
from models import Student  # make sure this matches your models file

api_public = Blueprint("api_public", __name__, url_prefix="/public")

# ✅ Public endpoint for student data
@api_public.route("/students", methods=["GET"])
def get_students():
    try:
        students = Student.query.all()
        result = [
            {
                "id": s.id,
                "name": s.name,
                "department": s.department,
                "semester": s.semester,
                "cgpa": s.cgpa,
                "hometown": s.hometown,
                "languages": s.languages_known,
            }
            for s in students
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Example dummy endpoints for Power BI (optional, you can add later)
@api_public.route("/marks", methods=["GET"])
def get_marks():
    marks_data = [
        {"student_id": 1, "semester": "Sem 1", "subject": "Maths", "marks": 82},
        {"student_id": 1, "semester": "Sem 1", "subject": "Programming", "marks": 88},
        {"student_id": 2, "semester": "Sem 2", "subject": "AI", "marks": 84},
    ]
    return jsonify(marks_data)


@api_public.route("/attendance", methods=["GET"])
def get_attendance():
    attendance_data = [
        {"student_id": 1, "total_days": 30, "present_days": 26, "percentage": 86.6},
        {"student_id": 2, "total_days": 30, "present_days": 28, "percentage": 93.3},
    ]
    return jsonify(attendance_data)
