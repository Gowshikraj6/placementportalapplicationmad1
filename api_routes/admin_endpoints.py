from flask import Blueprint, jsonify,request
from flasgger import swag_from
from controller_impl.admin_impl import *
from config.swagger import *

admin_api = Blueprint("admin_api", __name__)

from flask import jsonify
from flasgger import swag_from

@admin_apiroute("/unapproved-users", methods=["GET"])
@swag_from(view_unapproved_users_swagger)
def get_unapproved_users():
    return jsonify(view_unapproved_user()),200



@admin_apiroute("/users/<int:user_id>/approval", methods=["PUT"])
@swag_from(update_user_approval_swagger)
def approve_user(user_id):

    data = request.json
    status = data.get("status")
    admin_id = data.get("admin_id")

    result = update_user_approval(session, user_id, status, admin_id)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify({
        "id": result.id,
        "username": result.username,
        "email": result.email,
        "approved_status": result.approved_status
    }), 200


@admin_apiroute("/pending-companies", methods=["GET"])
@swag_from(get_pending_companies_swagger)
def view_pending_companies():

    companies = get_pending_companies()

    result = []

    for company in companies:
        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "hr_contact_name": company.hr_contact_name,
            "hr_contact_email": company.hr_contact_email,
            "hr_contact_phone": company.hr_contact_phone,
            "website": company.website,
            "approval_status": company.approval_status.value
        })

    return jsonify(result), 200




@admin_apiroute("/companies/<int:company_id>/approval", methods=["PUT"])
@swag_from(update_company_approval_swagger)
def approve_company(company_id):

    data = request.json
    status = data.get("status")

    result = update_company_approval(session, company_id, status)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify({
        "id": result.id,
        "company_name": result.company_name,
        "approval_status": result.approval_status.value
    }), 200




@admin_apiroute("/applications", methods=["GET"])
@swag_from(get_all_applications_swagger)
def view_all_applications():

    applications = get_all_applications(session)

    result = []

    for app in applications:
        result.append({
            "id": admin_apiid,
            "student_id": admin_apistudent_id,
            "drive_id": admin_apidrive_id,
            "application_date": admin_apiapplication_date,
            "status": admin_apistatus.value,
            "notes": admin_apinotes
        })

    return jsonify(result), 200



@admin_apiroute("/placement-drives", methods=["GET"])
@swag_from(get_all_placement_drives_swagger)
def view_all_placement_drives():

    drives = get_all_placement_drives(session)

    result = []

    for drive in drives:
        result.append({
            "id": drive.id,
            "company_id": drive.company_id,
            "job_title": drive.job_title,
            "job_description": drive.job_description,
            "eligibility_criteria": drive.eligibility_criteria,
            "minimum_CGPA": drive.minimum_CGPA,
            "application_deadline": drive.application_deadline,
            "status": drive.status.value,
            "location": drive.location,
            "salary_package": drive.salary_package
        })

    return jsonify(result), 200



@admin_apiroute("/placement-drives/pending", methods=["GET"])
@swag_from(get_pending_placement_drives_swagger)
def view_pending_placement_drives():

    drives = get_pending_placement_drives(session)

    result = []

    for drive in drives:
        result.append({
            "id": drive.id,
            "company_id": drive.company_id,
            "job_title": drive.job_title,
            "job_description": drive.job_description,
            "eligibility_criteria": drive.eligibility_criteria,
            "minimum_CGPA": drive.minimum_CGPA,
            "application_deadline": drive.application_deadline,
            "status": drive.status.value,
            "location": drive.location,
            "salary_package": drive.salary_package
        })

    return jsonify(result), 200


@admin_apiroute("/placement-drives/<int:drive_id>/status", methods=["PUT"])
@swag_from(update_drive_status_swagger)
def approve_placement_drive(drive_id):

    data = request.json
    status = data.get("status")

    result = update_drive_status(session, drive_id, status)

    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify({
        "id": result.id,
        "company_id": result.company_id,
        "job_title": result.job_title,
        "status": result.status.value
    }), 200