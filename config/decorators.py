from functools import wraps
from flask_jwt_extended import get_jwt, jwt_required

def role_required(role):

    def wrapper(fn):

        @wraps(fn)
        @jwt_required()   # <-- JWT verification already happens here
        def decorator(*args, **kwargs):

            claims = get_jwt()
            roles = claims.get("roles", [])

            if role not in roles:
                return {"message": "Forbidden"}, 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper