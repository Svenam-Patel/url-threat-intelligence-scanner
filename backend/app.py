from flask import Flask, request, jsonify
from flask_cors import CORS
from scanner import scan_url
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS scans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        score INTEGER,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/scan", methods=["POST"])
def scan():

    data = request.json
    url = data["url"]

    result = scan_url(url)

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    score = result.get("score", 0)

    cur.execute(
        "INSERT INTO scans(url,score,status) VALUES(?,?,?)",
        (url, score, result["status"])
    )

    conn.commit()
    conn.close()

    return jsonify(result)


@app.route("/history")
def history():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    rows = cur.execute(
        "SELECT * FROM scans ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)