from fastapi import FastAPI, Depends, Form, UploadFile
from database import engine, Base, get_db, MEDIA_DIR
from schemas import DoctorCreate, DoctorResponse, PatientCreate, PatientResponse
from models import *
from sqlalchemy.ext.asyncio import AsyncSession
import crud
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.mount(f"/{MEDIA_DIR}", StaticFiles(directory="media"), name="media")



@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/doctors/", response_model=list[DoctorResponse])
async def doctors(db: AsyncSession = Depends(get_db)):
    return await crud.read_doctors(db)

@app.get("/doctors/{doctor_id}", response_model=DoctorResponse)
async def doctor2(doctor_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.read_doctor(doctor_id, db)




@app.post("/doctors/", response_model=DoctorResponse)
async def pos(doc: DoctorCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_doctor(doc, db)


@app.put("/doctors/{doctor_id}", response_model=DoctorResponse)
async def upd(doctor_id: int, doc: DoctorCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_doctor(doctor_id, doc, db)



@app.delete("/doctors/{doctor_id}")
async def delet(doctor_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_doctor(doctor_id, db)










@app.get("/patients/", response_model=list[PatientResponse])
async def ol(db: AsyncSession = Depends(get_db)):
    return await crud.read_patients(db)


@app.get("/patients/{patient_id}", response_model=PatientResponse)
async def olmoq(patient_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.read_patient(patient_id, db)




@app.post("/patients/", response_model=PatientResponse)
async def kirit(pat: PatientCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_patient(pat, db)





@app.put("/patients/{patient_id}", response_model=PatientResponse)
async def upg(patient_id: int, pat: PatientCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_patient(patient_id, pat, db)


@app.delete("/patients/{patient_id}")
async def ochir(patient_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_patient(patient_id, db)




@app.post("/patient/", response_model=PatientResponse)
async def postin(
        full_name: str = Form(...),
        age: int = Form(...),
        doctor_id: int = Form(...),
        image: UploadFile  = None,
        video: UploadFile = None,
        db: AsyncSession = Depends(get_db)
):
    patient = PatientCreate(full_name=full_name, age=age,doctor_id=doctor_id, image=image, video=video, db=db)
    return await crud.creap(patient, db, image, video)
    







































if __name__=="__main__":
    uvicorn.run(app)