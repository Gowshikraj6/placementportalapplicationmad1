from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from config.admin_creation import create_admin
import traceback

Base = declarative_base()


def create_db_and_tables():
    try:
        engine = create_engine("sqlite:///placement23f1002989.db",echo=True)
        conn = engine.connect()
        print("Database created!")
        Base.metadata.create_all(engine)
        print("Tables created!")
        create_admin(engine)
        print("admin created")
    except Exception as e:
        print("Error occured !!!")
        traceback.print_exc()

