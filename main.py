from models import create_db_and_tables,engine
from flask import Flask
from api_routes.registration_endpoints import register_api
from flask_login import current_user,LoginManager,login_user
from flask import abort ,request
from flasgger import Swagger
from config.admin_creation import create_admin

create_db_and_tables()
create_admin(engine)
print("admin created")
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

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login")
def login():
    user = User.query.first()
    login_user(user)
    return "Logged in"

swagger = Swagger(app)

if __name__ == "__main__":
    app.run(debug=True)