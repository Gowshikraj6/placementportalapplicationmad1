from config.constants import roles, admin_role,company_role,description,student_role
from flask import abort,jsonify,request
from models.users import User
from models.roles import Role
from models.user_role import roles_users
from models.student import Student
from werkzeug.security import generate_password_hash
from datetime import datetime
from config.db_creation import session
from models.company import Company,ApprovalStatus
from models.application import Application
from models.company_user import CompanyUser
from config.db_creation import engine
import traceback
from models.placement_drive import PlacementDrive
from models.placement_drive import DriveStatus


def view_unapproved_user():
    users = session.query(User).filter(
        User.approved_status == "Pending"
    ).all()

    return [user.to_dict() for user in users]

def update_user_approval(session: session, user_id, status, admin_id):

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    user.approved_status = status
    user.approved_at = datetime.utcnow()
    user.approved_by = admin_id
    session.commit()
    return user.to_dict()


def get_pending_companies(session: session):

    companies = session.query(Company).filter(
        Company.approval_status == ApprovalStatus.PENDING
    ).all()
    return [company.to_dict() for company in companies]

def update_company_approval(session: session, company_id, status):

    company = session.query(Company).filter(
        Company.id == company_id
    ).first()
    if not company:
        return {"error": "Company not found"}
    company.approval_status = status
    company.updated_at = datetime.utcnow()
    session.commit()
    return company.to_dict()



def get_all_applications(session: session):

    applications = session.query(Application).all()
    return [application.to_dict() for application in applications]


def get_all_placement_drives(session: session):

    drives = session.query(PlacementDrive).all()

    return [drive.to_dict() for drive in drives]



def get_pending_placement_drives(session: session):

    drives = session.query(PlacementDrive).filter(
        PlacementDrive.status == DriveStatus.PENDING
    ).all()

    return [drive.to_dict() for drive in drives]


def update_drive_status(session: session, drive_id, status):

    drive = session.query(PlacementDrive).filter(
        PlacementDrive.id == drive_id
    ).first()
    if not drive:
        return {"error": "Placement drive not found"}
    drive.status = status
    session.commit()
    return drive.to_dict()