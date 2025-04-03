from sqlalchemy import Column, Integer, String, Date
from app.database.db import Base

class BetaTester(Base):
    __tablename__ = "beta_testers"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    dob = Column(Date)