from flask import Blueprint, jsonify,request
from flasgger import swag_from
from controller_impl.registation_impl import register_user

register_api = Blueprint("registration_api", __name__)

@register_api.route("/register_student", methods=["POST"])
@swag_from({
    "tags": ["Register"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {

                    "username": {
                        "type": "string",
                        "example": "gowshik123"
                    },
                    "role": {
                        "type": "string",
                        "example": "STUDENT"
                    },

                    "email": {
                        "type": "string",
                        "example": "gowshik@student.com"
                    },

                    "password": {
                        "type": "string",
                        "example": "password123"
                    },

                    "roll_number": {
                        "type": "string",
                        "example": "21CSE001"
                    },

                    "first_name": {
                        "type": "string",
                        "example": "Gowshik"
                    },

                    "last_name": {
                        "type": "string",
                        "example": "Raj"
                    },

                    "phone": {
                        "type": "string",
                        "example": "9876543210"
                    },

                    "department": {
                        "type": "string",
                        "example": "CSE"
                    },

                    "degree": {
                        "type": "string",
                        "example": "BTech"
                    },

                    "batch_year": {
                        "type": "integer",
                        "example": 2025
                    },

                    "cgpa": {
                        "type": "number",
                        "example": 8.5
                    },

                    "skills": {
                        "type": "string",
                        "example": "Python, SQL, React"
                    }

                },
                "required": [
                    "username",
                    "email",
                    "password",
                    "roll_number",
                    "first_name",
                    "phone",
                    "department",
                    "degree",
                    "batch_year"
                ]
            }
        }
    ],

    "responses": {
        201: {
            "description": "Student registered successfully"
        },
        400: {
            "description": "Validation error"
        }
    }
})
def register_user_field():
    data = request.json
    return register_user(data)


@register_api.route("/register_company", methods=["POST"])
@swag_from({
    "tags": ["Register"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {

                    "username": {
                        "type": "string",
                        "example": "hr_gowshik"
                    },
                    "role": {
                        "type": "string",
                        "example": "COMPANY"
                    },
                    "email": {
                        "type": "string",
                        "example": "hr@abctech.com"
                    },

                    "password": {
                        "type": "string",
                        "example": "password123"
                    },

                    "company_name": {
                        "type": "string",
                        "example": "ABC Technologies"
                    },

                    "website": {
                        "type": "string",
                        "example": "https://abctech.com"
                    },

                    "industry": {
                        "type": "string",
                        "example": "Information Technology"
                    },

                    "headquarters": {
                        "type": "string",
                        "example": "Chennai, India"
                    },

                    "description": {
                        "type": "string",
                        "example": "AI and Cloud solutions company"
                    }

                },
                "required": [
                    "username",
                    "email",
                    "password",
                    "company_name"
                ]
            }
        }
    ],

    "responses": {

        201: {
            "description": "User successfully linked to company",
            "examples": {
                "application/json": {
                    "message": "User successfully linked to company",
                    "user_id": 12,
                    "company_id": 3
                }
            }
        },

        400: {
            "description": "User already mapped to this company"
        },

        500: {
            "description": "Internal server error"
        }

    }
})
def register_user_company():
    data = request.json
    return register_user(data)