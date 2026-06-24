from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.db import fetch_one, fetch_all
from app.utils.responses import success

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.get("/summary")
@jwt_required()
def summary():
    user_id = get_jwt_identity()

    totals = fetch_one("""
        SELECT
            COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) AS total_income,
            COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0) AS total_expense
        FROM transactions
        WHERE user_id = %s
    """, (user_id,))

    category_expenses = fetch_all("""
        SELECT c.name, COALESCE(SUM(t.amount), 0) AS total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = %s AND t.type = 'expense'
        GROUP BY c.name
        ORDER BY total DESC
    """, (user_id,))

    income = float(totals["total_income"])
    expense = float(totals["total_expense"])

    return success("Dashboard summary fetched successfully", {
        "total_income": income,
        "total_expense": expense,
        "savings": income - expense,
        "category_expenses": category_expenses
    })