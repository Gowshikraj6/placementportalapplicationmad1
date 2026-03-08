from config.constants import roles, admin_role,company_role,description,student_role
from flask import abort,jsonify,request
from models.users import User
from models.roles import Role
from models.user_role import roles_users
from models.student import Student
from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy.orm import Session
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

    return users

def update_user_approval(session: Session, user_id, status, admin_id):

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    user.approved_status = status
    user.approved_at = datetime.utcnow()
    user.approved_by = admin_id
    session.commit()
    return user


def get_pending_companies(session: Session):

    companies = session.query(Company).filter(
        Company.approval_status == ApprovalStatus.PENDING
    ).all()
    return companies

def update_company_approval(session: Session, company_id, status):

    company = session.query(Company).filter(
        Company.id == company_id
    ).first()
    if not company:
        return {"error": "Company not found"}
    company.approval_status = status
    company.updated_at = datetime.utcnow()
    session.commit()
    return company



def get_all_applications(session: Session):

    applications = session.query(Application).all()
    return applications


def get_all_placement_drives(session: Session):

    drives = session.query(PlacementDrive).all()

    return drives



def get_pending_placement_drives(session: Session):

    drives = session.query(PlacementDrive).filter(
        PlacementDrive.status == DriveStatus.PENDING
    ).all()

    return drives


def update_drive_status(session: Session, drive_id, status):

    drive = session.query(PlacementDrive).filter(
        PlacementDrive.id == drive_id
    ).first()
    if not drive:
        return {"error": "Placement drive not found"}
    drive.status = status
    session.commit()
    return drive