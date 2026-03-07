from flask import Blueprint, jsonify

register_api = Blueprint("registration_api", __name__)

@register_api.route("/register", methods=["POST"])
def register_students():
    return jsonify({"message": "students list"})