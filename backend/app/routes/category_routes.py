from flask import Blueprint
from app.db import fetch_all
from app.utils.responses import success

category_bp = Blueprint("categories", __name__)

@category_bp.get("")
def list_categories():
    categories = fetch_all("SELECT id, name, type FROM categories ORDER BY type, name")
    return success("Categories fetched successfully", categories)