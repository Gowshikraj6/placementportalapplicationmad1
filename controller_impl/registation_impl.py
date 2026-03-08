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
from models.company_user import CompanyUser
from config.db_creation import engine
import traceback

def register_user(data):
    if data['role'] not in roles:
        abort(400, description="roles doesnt exist")

    if data['role'] ==admin_role:
        abort(400, description="role cannot be admin")

    session = Session(engine)

    try:
        
        approved_status = "Approved"
        if data['role'] == company_role:
            approved_status = "Pending"

        entry_role = session.query(Role).filter_by(name=data["role"]).first()

        # 2️⃣ Check if admin user exists
        admin_user = session.query(User).filter_by(username=data["username"]).first()

        if not admin_user:
            admin_user = User(
                username=data["username"],
                email=data["email"],
                password=generate_password_hash(data["password"]),
                active=True,
                approved_status=approved_status,
                created_by="SYSTEM"
            )

            session.add(admin_user)
            session.flush()  # Get the user ID without committing

            # Method 1: Using the relationship (should work)
            admin_user.roles.append(entry_role)

            # Optional auditing
            

            session.commit()
            print("user created successfully with role!")

            # Verify the association was created
            check_association = session.execute(
                roles_users.select().where(
                    roles_users.c.user_id == admin_user.id
                )
            ).first()
            print(f"Association created: {check_association is not None}")

        else:
            abort(400,description="user already exists")

            # Check if user already has the role
            has_role = session.execute(
                roles_users.select().where(
                    roles_users.c.user_id == admin_user.id,
                    roles_users.c.role_id == entry_role.id
                )
            ).first()

            if not has_role:
                # Method 2: Direct insert if relationship isn't working
                session.execute(
                    roles_users.insert().values(
                        user_id=admin_user.id,
                        role_id=entry_role.id
                    )
                )
                session.commit()
                print("role assigned to existing user via direct insert!")
            else:
                print("user already hasrole")

        if data['role'] ==student_role:
            return register_student(data)
        elif data['role'] ==company_role:
            return register_company(data)

    except Exception as e:
        session.rollback()
        print(f"Error creating user: {e}")
        print(traceback.format_exc())
        abort(500, description="Error creating user")
    finally:
        session.close()

def register_student(data):
    session = Session(engine)

    try:

        # -----------------------
        # 1️⃣ Check if USER exists
        # -----------------------
        user = session.query(User).filter_by(
            email=data["email"]
        ).first()

        if not user:
            user = User(
                username=data["username"],
                email=data["email"],
                password=generate_password_hash(data["password"]),
                approved_status="Approved"
            )

            session.add(user)
            session.flush()  # get user.id

        # -----------------------
        # 2️⃣ Check if STUDENT exists
        # -----------------------
        existing_student = session.query(Student).filter_by(
            user_id=user.id
        ).first()

        if existing_student:
            return jsonify({
                "error": "Student profile already exists for this user"
            }), 400

        # -----------------------
        # 3️⃣ Create Student
        # -----------------------
        student = Student(
            user_id=user.id,
            roll_number=data["roll_number"],
            first_name=data["first_name"],
            last_name=data.get("last_name"),
            email=data["email"],
            phone=data["phone"],
            gender=data.get("gender"),
            date_of_birth=data.get("date_of_birth"),

            department=data["department"],
            degree=data["degree"],
            specialization=data.get("specialization"),
            batch_year=data["batch_year"],

            cgpa=data.get("cgpa"),
            tenth_percentage=data.get("tenth_percentage"),
            twelfth_percentage=data.get("twelfth_percentage"),
            diploma_percentage=data.get("diploma_percentage"),

            active_backlogs=data.get("active_backlogs", 0),
            total_backlogs=data.get("total_backlogs", 0),

            placement_status="NOT_PLACED",
            willing_to_relocate=data.get("willing_to_relocate", True),

            github_url=data.get("github_url"),
            linkedin_url=data.get("linkedin_url"),
            portfolio_url=data.get("portfolio_url"),
            leetcode_rating=data.get("leetcode_rating"),
            hackerrank_rating=data.get("hackerrank_rating"),
            skills=data.get("skills")
        )

        session.add(student)
        session.commit()

        return jsonify({
            "message": "Student registered successfully",
            "user_id": user.id,
            "student_id": student.id
        }), 201

    except Exception as e:
        session.rollback()
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

def register_company(data):
    session = Session(engine)
    try:

        user = session.query(User).filter_by(
            email=data["email"]
        ).first()

        if not user:
            user = User(
                username=data["username"],
                email=data["email"],
                password=generate_password_hash(data["password"]),
                approved_status="Pending"
            )
            session.add(user)
            session.flush()  # get user.id

        # ---------- COMPANY CHECK ----------
        company = session.query(Company).filter_by(
            company_name=data["company_name"]
        ).first()

        if not company:
            company = Company(
                company_name=data["company_name"],
                website=data.get("website"),
                industry=data.get("industry"),
                headquarters=data.get("headquarters"),
                description=data.get("description"),
                approval_status=ApprovalStatus.PENDING
            )

            session.add(company)
            session.flush()  # get company.id

        # ---------- MAPPING CHECK ----------
        existing_mapping = session.query(CompanyUser).filter_by(
            user_id=user.id,
            company_id=company.id
        ).first()

        if existing_mapping:
            return jsonify({
                "message": "User already mapped to this company"
            }), 400

        company_user = CompanyUser(
            user_id=user.id,
            company_id=company.id
        )

        session.add(company_user)
        session.commit()

        return jsonify({
            "message": "User successfully linked to company",
            "user_id": user.id,
            "company_id": company.id
        }), 201

    except Exception as e:
        session.rollback()
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()