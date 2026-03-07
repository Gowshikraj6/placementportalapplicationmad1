from sqlalchemy.orm import Session
from models.users import User
from models.roles import Role
from models.user_role import roles_users

def create_admin(engine):

    session = Session(engine)

    admin_role = session.query(Role).filter_by(name="ADMIN").first()

    if not admin_role:
        admin_role = Role(name="ADMIN")
        session.add(admin_role)
        session.commit()

    admin_user = session.query(User).filter_by(username="admin").first()

    if not admin_user:
        admin_user = User(username="admin", password="admin123")
        session.add(admin_user)
        session.commit()

        user_role = roles_users(
            user_id=admin_user.id,
            role_id=admin_role.id
        )

        session.add(user_role)
        session.commit()

    session.close()