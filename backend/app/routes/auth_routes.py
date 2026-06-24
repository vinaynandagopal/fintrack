from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import fetch_one, execute_query
from app.utils.responses import success, error

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not full_name or not email or not password:
        return error("Full name, email, and password are required", 400)

    if len(password) < 6:
        return error("Password must be at least 6 characters", 400)

    existing = fetch_one("SELECT id FROM users WHERE email = %s", (email,))
    if existing:
        return error("Email is already registered", 409)

    password_hash = generate_password_hash(password)
    user_id = execute_query(
        "INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
        (full_name, email, password_hash),
    )

    token = create_access_token(identity=str(user_id))
    return success("User registered successfully", {
        "token": token,
        "user": {"id": user_id, "full_name": full_name, "email": email}
    }, 201)

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = fetch_one("SELECT * FROM users WHERE email = %s", (email,))
    if not user or not check_password_hash(user["password_hash"], password):
        return error("Invalid email or password", 401)

    token = create_access_token(identity=str(user["id"]))
    return success("Login successful", {
        "token": token,
        "user": {"id": user["id"], "full_name": user["full_name"], "email": user["email"]}
    })

@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = fetch_one("SELECT id, full_name, email, created_at FROM users WHERE id = %s", (user_id,))
    if not user:
        return error("User not found", 404)
    return success("Profile fetched successfully", user)