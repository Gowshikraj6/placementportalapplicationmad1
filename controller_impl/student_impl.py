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