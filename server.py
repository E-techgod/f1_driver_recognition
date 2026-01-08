import sqlite3
from pathlib import Path
from flask_cors import CORS
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)
portID= 5006

# SQLite database path
def get_today_db_path():
    date_str = datetime.now().strftime('%Y-%m-%d')
    attendance_dir = Path(__file__).resolve().parent / "Attendance"
    attendance_dir.mkdir(parents=True, exist_ok=True)
    return str(attendance_dir / f"attendance_{date_str}.db")

# Initialize the SQLite database
def init_db():
    db_path= get_today_db_path();
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Log attendance
@app.route('/attendance', methods=['POST'])
def log_attendance():
    data = request.json
    driver = data.get("driver_name")
    timestamp = data.get("timestamp") or datetime.now().isoformat()

    db_path= get_today_db_path();
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO attendance (driver_name, timestamp) VALUES (?, ?)', (driver, timestamp))
    conn.commit()
    conn.close()

    print(f"Stored: {driver} at {timestamp}")
    return jsonify({"status": "success"})

# View all attendance entries
@app.route('/attendance', methods=['GET'])
def view_attendance():

    db_path= get_today_db_path();
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT driver_name, timestamp FROM attendance ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()

    # Convert to list of dicts
    result = [{"driver_name": r[0], "timestamp": r[1]} for r in rows]
    return jsonify(result)

if __name__ == '__main__':
    print("Flask with SQLite starting...")
    app.run(debug=True, port=portID)
