from flask import Blueprint, request, jsonify
from models import Student
import re

ai_bp = Blueprint("ai_bp", __name__)

@ai_bp.route("/ai/respond", methods=["POST"])
def ai_respond():
    data = request.get_json()
    question = data.get("question", "").lower()
    student_id = data.get("student_id")

    s = Student.query.get(student_id)
    if not s:
        return jsonify({"reply": "Sorry, I couldn’t find that student."}), 404

    # Convert to dict for easier use
    stud = s.to_dict()

    # --- SMART LOGIC ---
    if "cgpa" in question:
        return jsonify({"reply": f"Your current CGPA is {stud.get('cgpa', 'not available')}."})

    if "attendance" in question:
        att = stud.get("attendance_semester", "not recorded")
        return jsonify({"reply": f"Your attendance this semester is {att}."})

    if "seminar" in question:
        return jsonify({"reply": "Your next seminar is 'AI Workshop' on 2025-11-12."})

    if "holiday" in question:
        return jsonify({"reply": "Upcoming holidays include Diwali on Nov 5 and Christmas on Dec 25."})

    if "timetable" in question:
        timetable = stud.get("timetable", [])
        if not timetable:
            return jsonify({"reply": "Your timetable is not available yet."})
        formatted = ", ".join([f"{t['day']}: {t['class']} at {t['time']}" for t in timetable])
        return jsonify({"reply": f"Here’s your timetable: {formatted}."})

    if "book" in question or "library" in question:
        books = stud.get("library_books", [])
        if not books:
            return jsonify({"reply": "You haven’t borrowed any books yet."})
        return jsonify({"reply": f"You currently have {len(books)} book(s): {', '.join(books)}."})

    # Fallback
    return jsonify({"reply": "I'm still learning to answer that! Try asking about CGPA, attendance, or timetable."})
