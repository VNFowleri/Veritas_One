from sqlalchemy import Column, Integer, String, DateTime, Text, LargeBinary  # ✅ Add LargeBinary
from app.database.db import Base
from datetime import datetime

class FaxFile(Base):
    __tablename__ = "fax_files"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    received_time = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String, nullable=False)
    pdf_data = Column(LargeBinary, nullable=True)  # ✅ This is the fix
    ocr_text = Column(Text, nullable=True)