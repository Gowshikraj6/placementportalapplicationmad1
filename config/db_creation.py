from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
import traceback

Base = declarative_base()
engine = create_engine("sqlite:///placement23f1002989.db",echo=True)
session = Session(engine)
