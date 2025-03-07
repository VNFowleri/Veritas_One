from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+pg8000://user:password@localhost/dbname")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class FaxFile(Base):
    __tablename__ = "fax_files"

    id = Column(Integer, primary_key=True, index=True)
    twilio_fax_id = Column(String, unique=True, nullable=True)  # Twilio Fax ID
    file_path = Column(String, nullable=False)  # Path to stored PDF
    raw_text = Column(Text, nullable=True)  # OCR-extracted text
    created_at = Column(DateTime, default=datetime.utcnow)


class DeidentifiedFile(Base):
    __tablename__ = "deidentified_files"

    id = Column(Integer, primary_key=True, index=True)
    fax_file_id = Column(Integer, ForeignKey("fax_files.id"), nullable=False)
    deidentified_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)