from flask import Blueprint, jsonify
from flasgger import swag_from
from controller_impl.registation_impl import register_student
register_api = Blueprint("registration_api", __name__)

@register_api.route("/register", methods=["POST"])
@swag_from({
    "responses": {
        200: {
            "description": "Registrations"
        }
    }
})
def register_user():
    data = request.json
    return register_student(data)