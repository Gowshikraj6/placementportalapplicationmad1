from config.constants import roles
from flask import abort


def register_student(data):
    if data['role'] not in roles:
        abort(400, description="roles doesnt exist")

    session = Session(engine)

    try:


        entry_role = Role(
                name="ADMIN",
                description="System Administrator"
            )
        session.add(admin_role)
        session.commit()  # Commit to ensure role exists
        print("ADMIN role created")

        # 2️⃣ Check if admin user exists
        admin_user = session.query(User).filter_by(username="admin").first()

        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@placement.com",
                password=generate_password_hash("admin123"),
                active=True,
                is_approved=True,
                created_by="SYSTEM"
            )

            session.add(admin_user)
            session.flush()  # Get the user ID without committing

            # Method 1: Using the relationship (should work)
            admin_user.roles.append(admin_role)

            # Optional auditing
            admin_user.approved_by = admin_user.id
            admin_user.approved_at = datetime.utcnow()

            session.commit()
            print("Admin user created successfully with ADMIN role!")

            # Verify the association was created
            check_association = session.execute(
                roles_users.select().where(
                    roles_users.c.user_id == admin_user.id
                )
            ).first()
            print(f"Association created: {check_association is not None}")

        else:
            print("Admin user already exists")

            # Check if user already has the role
            has_role = session.execute(
                roles_users.select().where(
                    roles_users.c.user_id == admin_user.id,
                    roles_users.c.role_id == admin_role.id
                )
            ).first()

            if not has_role:
                # Method 2: Direct insert if relationship isn't working
                session.execute(
                    roles_users.insert().values(
                        user_id=admin_user.id,
                        role_id=admin_role.id
                    )
                )
                session.commit()
                print("ADMIN role assigned to existing admin user via direct insert!")
            else:
                print("Admin user already has ADMIN role")

    except Exception as e:
        session.rollback()
        print(f"Error creating user: {e}")
        abort(500, description="Error creating user")
    finally:
        session.close()
