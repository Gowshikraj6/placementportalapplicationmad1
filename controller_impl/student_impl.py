from sqlalchemy.orm import Session
from models.application import Application
from models.enums import ApplicationStatus


def apply_for_drive(session: Session, student_id, drive_id,notes:None):

    # 🔹 Check if student already applied
    existing_application = session.query(Application).filter(
        Application.student_id == student_id,
        Application.drive_id == drive_id
    ).first()

    if existing_application:
        return {"error": "Student already applied for this placement drive"}

    # 🔹 Create new application
    application = Application(
        student_id=student_id,
        drive_id=drive_id,
        status=ApplicationStatus.APPLIED,
        notes = notes
    )

    session.add(application)
    session.commit()

    return application


from sqlalchemy.orm import Session
from models.student import Student


def update_student(session: Session, student_id, data):

    student = session.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        return {"error": "Student not found"}

    # Update fields dynamically
    for key, value in data.items():
        if hasattr(student, key):
            setattr(student, key, value)

    session.commit()

    return student


from sqlalchemy.orm import Session
from models.placement_drive import PlacementDrive, DriveStatus


def get_approved_drives(session: Session):
    try:
        drives = (
            session.query(PlacementDrive)
            .filter(PlacementDrive.status == DriveStatus.APPROVED)
            .all()
        )

        result = []

        for drive in drives:
            result.append({
                "id": drive.id,
                "company_name": drive.company.company_name if drive.company else None,
                "job_title": drive.job_title,
                "job_description": drive.job_description,
                "eligibility_criteria": drive.eligibility_criteria,
                "minimum_CGPA": drive.minimum_CGPA,
                "application_deadline": drive.application_deadline,
                "location": drive.location,
                "salary_package": drive.salary_package,
                "status": drive.status.value,
                "created_at": drive.created_at
            })

        return result

    except Exception as e:
        return {"error": str(e)}


from sqlalchemy.orm import Session
from models.application import Application
from models.placement_drive import PlacementDrive


def get_student_applications(session: Session, student_id: int):
    try:
        applications = (
            session.query(Application)
            .join(Application.drive)
            .filter(Application.student_id == student_id)
            .all()
        )

        result = []

        for app in applications:
            drive = app.drive

            result.append({
                "application_id": app.id,
                "application_date": app.application_date,
                "application_status": app.status.value,

                "drive": {
                    "drive_id": drive.id,
                    "job_title": drive.job_title,
                    "company_name": drive.company.company_name if drive.company else None,
                    "location": drive.location,
                    "salary_package": drive.salary_package,
                    "application_deadline": drive.application_deadline
                },

                "notes": app.notes
            })

        return result

    except Exception as e:
        return {"error": str(e)}