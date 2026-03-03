from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contacts (name, email, message, created_at)
        VALUES (?, ?, ?, ?)
    """, (name, email, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return jsonify({"message": "Message sent successfully!"})

@app.route("/download-resume")
def download_resume():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "static", "resume.pdf")

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Resume file not found in static folder", 404


# ===== VERY IMPORTANT PART =====
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Serve certificate files
@app.route('/static/certificates/<path:filename>')
def certificates(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/certificates'), filename)

if __name__ == '__main__':
    app.run(debug=True)
    
if __name__ == "__main__":
    app.run(debug=True)