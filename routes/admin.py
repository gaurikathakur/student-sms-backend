# backend/routes/admin.py
from flask import Blueprint, request, jsonify
from models import db, Student
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin_bp", __name__)

# Get all students (admins can view everything)
@admin_bp.route("/students", methods=["GET"])
def get_students():
    students = Student.query.filter(Student.role != "admin").all()
    return jsonify([s.to_dict() for s in students])

# Get single student (admin)
@admin_bp.route("/student/<int:id>", methods=["GET"])
def get_student(id):
    s = Student.query.get(id)
    if not s:
        return jsonify({"error":"not found"}),404
    return jsonify({"student": s.to_dict()})

# Promote student to admin
@admin_bp.route("/promote/<int:id>", methods=["PUT"])
def promote(id):
    s = Student.query.get(id)
    if not s:
        return jsonify({"error":"not found"}),404
    s.role = "admin"
    db.session.commit()
    return jsonify({"message":"promoted","student": s.to_dict()})

# Edit student details
@admin_bp.route("/edit/<int:id>", methods=["PUT"])
def edit_student(id):
    s = Student.query.get(id)
    if not s:
        return jsonify({"error":"not found"}),404
    data = request.json or {}
    for k in ["name","department","semester","cgpa","hometown","current_address","dob","mobile"]:
        if k in data:
            setattr(s, k, data[k])
    db.session.commit()
    return jsonify({"message":"updated","student": s.to_dict()})

# Delete student
@admin_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_student(id):
    s = Student.query.get(id)
    if not s:
        return jsonify({"error":"not found"}),404
    db.session.delete(s)
    db.session.commit()
    return jsonify({"message":"deleted"})
