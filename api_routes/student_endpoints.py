from flask import Blueprint, jsonify,request
from flasgger import swag_from
from controller_impl.student_impl import *
from config.swagger import *


student_api = Blueprint("student_api", __name__)



@student_api.route("/student/drives", methods=["GET"])
@swag_from(get_approved_drives_swagger)
def fetch_approved_drives():

    result = get_approved_drives(session)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 500

    return jsonify(result), 200



@student_api.route("/student/apply", methods=["POST"])
@swag_from(apply_for_drive_swagger)
def apply_drive():

    data = request.json

    student_id = data.get("student_id")
    drive_id = data.get("drive_id")
    notes = data.get("notes")

    result = apply_for_drive(session, student_id, drive_id, notes)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 400

    return jsonify({
        "id": result.id,
        "student_id": result.student_id,
        "drive_id": result.drive_id,
        "status": result.status.value,
        "notes": result.notes
    }), 201


@student_api.route("/student/<int:student_id>", methods=["PUT"])
@swag_from(update_student_swagger)
def update_student_profile(student_id):

    data = request.json

    result = update_student(session, student_id, data)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify({
        "id": result.id,
        "name": result.name,
        "email": result.email,
        "department": result.department,
        "cgpa": result.cgpa
    }), 200




@student_api.route("/student/<int:student_id>/applications", methods=["GET"])
@swag_from(get_student_applications_swagger)
def fetch_student_applications(student_id):

    result = get_student_applications(session, student_id)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 500

    return jsonify(result), 200