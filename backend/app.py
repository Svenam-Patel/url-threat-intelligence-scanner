from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import re
import socket

app = Flask(__name__)
CORS(app)

# ---------- DB ----------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # NOTE: no created_at dependency
    c.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        score INTEGER,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- HELPERS ----------
def extract_domain(url):
    try:
        return url.split("//")[-1].split("/")[0].lower()
    except:
        return ""

def normalize(name):
    replacements = {
        "0": "o", "1": "l", "3": "e",
        "5": "s", "@": "a", "7": "t"
    }
    for k, v in replacements.items():
        name = name.replace(k, v)
    return name

def advanced_checks(url):
    domain = extract_domain(url)
    name = domain.split(".")[0]

    score = 0
    reasons = []

    normalized = normalize(name)

    if normalized != name:
        score += 2
        reasons.append("Character substitution")

    if re.search(r"(.)\1{2,}", name):
        score += 2
        reasons.append("Repeated characters")

    if "rn" in name or "vv" in name:
        score += 2
        reasons.append("Visual spoofing")

    if re.search(r"\d{3,}", name):
        score += 2
        reasons.append("Too many numbers")

    if len(name) > 20:
        score += 1
        reasons.append("Long domain name")

    if name.count("-") >= 2:
        score += 2
        reasons.append("Hyphen abuse")

    try:
        socket.gethostbyname(domain)
    except:
        score += 3
        reasons.append("Domain does not resolve")

    return score, reasons

# ---------- ANALYZER ----------
def analyze_url(url):
    score = 0
    reasons = []

    if len(url) > 75:
        score += 2
        reasons.append("Long URL")

    if "@" in url:
        score += 3
        reasons.append("Contains @")

    if url.startswith("http://"):
        score += 2
        reasons.append("Not HTTPS")

    if len(url.split(".")) > 5:
        score += 2
        reasons.append("Too many subdomains")

    if re.search(r"(login|verify|secure|bank)", url):
        score += 2
        reasons.append("Suspicious keywords")

    extra_score, extra_reasons = advanced_checks(url)
    score += extra_score
    reasons.extend(extra_reasons)

    status = "Suspicious" if score >= 4 else "Safe"

    return {
        "url": url,
        "score": score,
        "status": status,
        "reasons": reasons
    }

# ---------- AUTH ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    user = c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    ).fetchone()

    conn.close()
    return jsonify({"success": True if user else False})

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (NULL, ?, ?)",
                  (data["username"], data["password"]))
        conn.commit()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False})

# ---------- ROUTES ----------
@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    result = analyze_url(data["url"])

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO scans (url, score, status) VALUES (?, ?, ?)",
              (data["url"], result["score"], result["status"]))
    conn.commit()
    conn.close()

    return jsonify(result)

@app.route("/history")
def history():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    rows = c.execute("SELECT * FROM scans ORDER BY id DESC").fetchall()
    conn.close()

    return jsonify([
        {"url": r[1], "score": r[2], "status": r[3]}
        for r in rows
    ])

@app.route("/stats")
def stats():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    total = c.execute("SELECT COUNT(*) FROM scans").fetchone()[0]
    safe = c.execute("SELECT COUNT(*) FROM scans WHERE status='Safe'").fetchone()[0]
    suspicious = c.execute("SELECT COUNT(*) FROM scans WHERE status='Suspicious'").fetchone()[0]

    conn.close()

    return jsonify({
        "total": total,
        "safe": safe,
        "suspicious": suspicious
    })

if __name__ == "__main__":
    app.run(debug=True)
