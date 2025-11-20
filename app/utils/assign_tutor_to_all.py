from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.student_model import Student

TUTOR_ID = 2  # ID del tutor que quieres asignar a todos


def assign_tutor_to_all():
    db: Session = SessionLocal()
    try:
        print(f"🔄 Asignando tutor_id={TUTOR_ID} a todos los estudiantes...")

        students = db.query(Student).all()
        total = len(students)

        if total == 0:
            print("⚠ No hay estudiantes en la base de datos.")
            return

        for s in students:
            s.tutor_id = TUTOR_ID

        db.commit()
        print(f"🎉 Listo: {total} estudiantes actualizados correctamente.")

    except Exception as e:
        print("❌ Error asignando tutor:", e)
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    assign_tutor_to_all()
