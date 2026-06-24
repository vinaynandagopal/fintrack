from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.db import fetch_all, fetch_one, execute_query
from app.utils.responses import success, error

transaction_bp = Blueprint("transactions", __name__)

@transaction_bp.get("")
@jwt_required()
def list_transactions():
    user_id = get_jwt_identity()
    rows = fetch_all("""
        SELECT t.id, t.type, t.amount, t.description, t.transaction_date,
               c.id AS category_id, c.name AS category_name
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = %s
        ORDER BY t.transaction_date DESC, t.id DESC
    """, (user_id,))
    return success("Transactions fetched successfully", rows)

@transaction_bp.post("")
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    category_id = data.get("category_id")
    tx_type = data.get("type")
    amount = data.get("amount")
    description = data.get("description", "")
    transaction_date = data.get("transaction_date")

    if tx_type not in ("income", "expense"):
        return error("Transaction type must be income or expense", 400)

    if not category_id or not amount or not transaction_date:
        return error("Category, amount, and transaction date are required", 400)

    category = fetch_one("SELECT id FROM categories WHERE id = %s AND type = %s", (category_id, tx_type))
    if not category:
        return error("Invalid category for transaction type", 400)

    tx_id = execute_query("""
        INSERT INTO transactions (user_id, category_id, type, amount, description, transaction_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, category_id, tx_type, amount, description, transaction_date))

    return success("Transaction created successfully", {"id": tx_id}, 201)

@transaction_bp.delete("/<int:transaction_id>")
@jwt_required()
def delete_transaction(transaction_id):
    user_id = get_jwt_identity()
    existing = fetch_one("SELECT id FROM transactions WHERE id = %s AND user_id = %s", (transaction_id, user_id))
    if not existing:
        return error("Transaction not found", 404)

    execute_query("DELETE FROM transactions WHERE id = %s AND user_id = %s", (transaction_id, user_id))
    return success("Transaction deleted successfully")