from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, UploadFile
from pathlib import Path
import shutil

from models import Doctor, Patient
from schemas import DoctorCreate, DoctorResponse, PatientCreate, PatientResponse
from database import *


async def cr(doc: DoctorCreate, db: AsyncSession):
    db_doc = Doctor(**doc.model_dump())
    db.add(db_doc)
    await db.commit()
    await db.refresh(db_doc)
    return db_doc

async def doc(db: AsyncSession):
    result = await db.execute(select(Doctor))
    return result.scalars().all()

async def doc2(doctor_id: int, db: AsyncSession):
    doctor = await db.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="not fond")
    return doctor

async def updat(doctor_id: int, doc: DoctorCreate, db: AsyncSession):
    doctor = await db.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for key, value in doc.model_dump().items():
        setattr(doctor, key, value)
    await db.commit()
    await db.refresh(doctor)
    return doctor

async def dele(doctor_id: int, db: AsyncSession):
    doctor = await db.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    await db.delete(doctor)
    await db.commit()
    return doctor


async def creap(pat: PatientCreate, db: AsyncSession, image:UploadFile=None, video:UploadFile=None):
    if image:
        image_extension = image.filename.lower().split(".")[-1]
        if image_extension not in ["jpg", "jpeg", "png"]:
            raise HTTPException(status_code=400, detail="faqat quyidagilar: jpg, jpeg, png")
    
    if video:
        video_extension = video.filename.lower().split(".")[-1]
        if video_extension not in ["mp4"]:
            raise HTTPException(status_code=400, detail="faqat mp4")


    db_pat = Patient(**pat.model_dump())
    db.add(db_pat)
    await db.commit()
    await db.refresh(db_pat)
    

    if image:
        image_path = Path(MEDIA_DIR) / f"patient_{db_pat.id}_image.{image_extension}"
        with image_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        db_pat.image = str(image_path)

    
    if video:
        video_path = Path(MEDIA_DIR) / f"patient_{db_pat.id}_video.{video_extension}"
        with video_path.open("wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        db_pat.video = str(video_path)

    await db.commit()
    await db.refresh(db_pat)
    return PatientResponse.model_validate(db_pat)






async def rel(db: AsyncSession):
    result = await db.execute(select(Patient))
    return result.scalars().all()

async def oq(patient_id: int, db: AsyncSession):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient




async def updat(patient_id: int, pat: PatientCreate, db: AsyncSession):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in pat.model_dump().items():
        setattr(patient, key, value)
    await db.commit()
    await db.refresh(patient)
    return patient




async def delen(patient_id: int, db: AsyncSession):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="not found")
    
    await db.delete(patient)
    await db.commit()
    return patient


