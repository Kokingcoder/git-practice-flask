import os
import sqlite3

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("routes", __name__)


def get_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    name = data.get("name")
    password = data.get("password")

    # input validation: email and password required
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    password_hash = generate_password_hash(password)

    db = get_db()
    try:
        cursor = db.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
            (email, name, password_hash),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "account with that email already exists"}), 409
    finally:
        db.close()

    return jsonify({
        "id": cursor.lastrowid,
        "email": email,
        "name": name,
    }), 201


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    db = get_db()
    cursor = db.execute(
        "SELECT id, email, name, password_hash FROM users WHERE email = ?",
        (email,),
    )
    user = cursor.fetchone()
    db.close()

    # generic failure if user not found OR password wrong
    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "invalid email or password"}), 401

    # success: return safe identity only
    return jsonify({
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
    }), 200