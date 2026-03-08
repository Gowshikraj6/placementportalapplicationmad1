from sqlalchemy.orm import Session
from datetime import datetime
from models.placement_drive import PlacementDrive
from models.application import Application
from models.student import Student

def create_placement_drive(session: Session, data):

    drive = PlacementDrive(
        company_id=data["company_id"],
        job_title=data["job_title"],
        job_description=data.get("job_description"),
        eligibility_criteria=data.get("eligibility_criteria"),
        minimum_CGPA=data.get("minimum_CGPA"),
        application_deadline=data.get("application_deadline"),
        location=data.get("location"),
        salary_package=data.get("salary_package")
    )

    session.add(drive)
    session.commit()

    return drive



def get_drives_by_company(session: Session, company_id):

    drives = session.query(PlacementDrive).filter(
        PlacementDrive.company_id == company_id
    ).all()
    return drives



def get_applications_by_drive(session: Session, drive_id):

    applications = session.query(Application).filter(
        Application.drive_id == drive_id
    ).all()

    return applications



def get_student_by_id(session: Session, student_id):

    student = session.query(Student).filter(
        Student.id == student_id
    ).first()

    return student


def update_application_status(session: Session, application_id, status):

    application = session.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application:
        return {"error": "Application not found"}

    application.status = status

    session.commit()

    return application