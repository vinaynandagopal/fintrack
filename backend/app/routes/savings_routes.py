from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.db import fetch_all, execute_query
from app.utils.responses import success, error

savings_bp = Blueprint("savings", __name__)

@savings_bp.get("")
@jwt_required()
def list_goals():
    user_id = get_jwt_identity()
    rows = fetch_all("""
        SELECT id, goal_name, target_amount, current_amount, target_date
        FROM savings_goals
        WHERE user_id = %s
        ORDER BY id DESC
    """, (user_id,))
    return success("Savings goals fetched successfully", rows)

@savings_bp.post("")
@jwt_required()
def create_goal():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    goal_name = data.get("goal_name", "").strip()
    target_amount = data.get("target_amount")
    current_amount = data.get("current_amount", 0)
    target_date = data.get("target_date")

    if not goal_name or not target_amount:
        return error("Goal name and target amount are required", 400)

    goal_id = execute_query("""
        INSERT INTO savings_goals (user_id, goal_name, target_amount, current_amount, target_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, goal_name, target_amount, current_amount, target_date))

    return success("Savings goal created successfully", {"id": goal_id}, 201)