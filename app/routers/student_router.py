from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.student_model import Student
from app.schemas.student_schema import StudentCreate, StudentResponse

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_st = Student(**student.dict())
    db.add(new_st)
    db.commit()
    db.refresh(new_st)
    return new_st
