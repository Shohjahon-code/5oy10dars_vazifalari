from typing import Optional, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Doctor(Base):
    __tablename__ = "doctor"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50))
    specialization: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    patients: Mapped[List["Patient"]] = relationship(back_populates="doctor")


class Patient(Base):
    __tablename__ = "patient"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column()
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctor.id"))

    image: Mapped[Optional[str]] = mapped_column(nullable=True)
    video: Mapped[Optional[str]] = mapped_column(nullable=True)
    

    doctor: Mapped["Doctor"] = relationship(back_populates="patients")


