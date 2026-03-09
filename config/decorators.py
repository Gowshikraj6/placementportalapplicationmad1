from functools import wraps
from flask_jwt_extended import get_jwt, jwt_required
import traceback


def role_required(role):

    def wrapper(fn):

        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):

            try:
                claims = get_jwt()
                roles = claims.get("roles", [])

                if role not in roles:
                    return {
                        "message": "Forbidden",
                        "required_role": role
                    }, 403

                return fn(*args, **kwargs)

            except Exception as e:

                print("Error in role_required decorator")
                traceback.print_exc()   # prints full stack trace in console/logs

                return {
                    "message": "Internal server error"
                }, 500

        return decorator

    return wrapper