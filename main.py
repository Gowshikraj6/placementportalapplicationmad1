from models import create_db_and_tables,engine
from flask import Flask
from api_routes.registration_endpoints import register_api
from api_routes.admin_endpoints import admin_api
from api_routes.company_endpoints import company_api
from api_routes.student_endpoints import student_api
from flask_login import current_user,LoginManager,login_user
from flask import abort ,request
from flasgger import Swagger,swag_from
from models.users import User
from config.admin_creation import create_admin
from config.db_creation import session
from config.swagger import swagger_template,login_doc
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

create_db_and_tables()
create_admin(engine)
print("admin created")
app = Flask(__name__)

app.register_blueprint(register_api, url_prefix="/register")
app.register_blueprint(admin_api, url_prefix="/admin")
app.register_blueprint(student_api, url_prefix="/student")
app.register_blueprint(company_api, url_prefix="/company")

app.config["JWT_SECRET_KEY"] = "#MAD!1@PROJECT*^$"





@app.route("/login", methods=["POST"])
@swag_from(login_doc)
def login():

    data = request.json

    user = session.query(User).filter_by(
        username=data["username"]
    ).first()

    if not user:
        return {"message": "User not found"}, 404

    if not check_password_hash(user.password, data["password"]):
        return {"message": "Invalid password"}, 401

    if user.approved_status != "Approved":
        return {"message": "User not approved"}, 403

    roles = [role.name for role in user.roles]

    token = create_access_token(
        identity=user.id,
        additional_claims={
            "roles": roles
        }
    )

    return {
        "access_token": token,
        "roles": roles
    }


swagger = Swagger(app,template=swagger_template)
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run(debug=True)