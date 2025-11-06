import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db


def create_app():
    app = Flask(__name__)

    # ✅ Enable CORS globally (no duplicate headers)
    CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"], supports_credentials=True)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # ✅ Import and register blueprints
    from routes.admin import admin_bp
    from routes.student import student_bp
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(student_bp, url_prefix="/api/student")

    # ✅ AI Chat Route (working CORS & JSON)
    @app.route("/api/ai/respond", methods=["POST"])
    def ai_respond():
        try:
            data = request.get_json(force=True)
            msg = (data.get("message") or "").lower().strip()

            if "attendance" in msg:
                reply = "📊 You can check your attendance chart in your dashboard!"
            elif "holiday" in msg:
                reply = "🎉 Upcoming holidays are listed in the Holidays section."
            elif "marks" in msg or "score" in msg:
                reply = "🧾 You can find your marks under the 'Marks' section of your dashboard."
            elif "timetable" in msg:
                reply = "🕒 Your timetable is displayed in your dashboard timetable section."
            elif "professor" in msg or "teacher" in msg:
                reply = "👨‍🏫 Professors’ details and experience are listed under the Professor Details section."
            else:
                reply = "🤖 Hi! I'm your AI Assistant. You can ask me about marks, attendance, timetable, or professors."

            return jsonify({"response": reply})

        except Exception as e:
            print("AI Error:", e)
            return jsonify({"error": str(e)}), 500

    @app.route("/")
    def home():
        return jsonify({"message": "✅ Student Management System backend is running!"})

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
