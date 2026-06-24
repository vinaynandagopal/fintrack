from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.db import fetch_all, execute_query
from app.utils.responses import success, error

budget_bp = Blueprint("budgets", __name__)

@budget_bp.get("")
@jwt_required()
def list_budgets():
    user_id = get_jwt_identity()
    rows = fetch_all("""
        SELECT b.id, b.month_year, b.amount, c.id AS category_id, c.name AS category_name
        FROM budgets b
        JOIN categories c ON b.category_id = c.id
        WHERE b.user_id = %s
        ORDER BY b.month_year DESC, c.name
    """, (user_id,))
    return success("Budgets fetched successfully", rows)

@budget_bp.post("")
@jwt_required()
def upsert_budget():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    category_id = data.get("category_id")
    month_year = data.get("month_year")
    amount = data.get("amount")

    if not category_id or not month_year or not amount:
        return error("Category, month_year, and amount are required", 400)

    execute_query("""
        INSERT INTO budgets (user_id, category_id, month_year, amount)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE amount = VALUES(amount)
    """, (user_id, category_id, month_year, amount))

    return success("Budget saved successfully", None, 201)