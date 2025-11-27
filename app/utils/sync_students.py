from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user_model import User
from app.models.student_model import Student


def sync_students():
    db: Session = SessionLocal()

    users = db.query(User).filter(User.role == "student").all()
    existing = {s.user_id for s in db.query(Student).all()}

    created = 0

    for u in users:
        if u.id not in existing:
            new_st = Student(nombre=u.name, user_id=u.id)
            db.add(new_st)
            created += 1

    db.commit()
    print(f"✔ Estudiantes sincronizados: {created}")


if __name__ == "__main__":
    sync_students()
