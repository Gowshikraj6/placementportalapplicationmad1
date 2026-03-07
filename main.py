from config.db_creation import create_engine
from flask import Flask
from api_routes.registration_endpoints import register_api
from flask_login import current_user
from flask import abort ,request

create_engine()

app = Flask(__name__)

app.register_blueprint(register_api, url_prefix="/register")

PUBLIC_ENDPOINTS = [
    "registration_api.register",
    "security.login",
    "static"
]

@app.before_request
def check_user_approval():
    if request.endpoint in PUBLIC_ENDPOINTS:
        return

    if current_user.is_authenticated:
        if not current_user.is_approved:
            abort(403, description="User not approved by admin")