import random
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.student_model import Student

TOTAL = 103

NOMBRES = [
    "Juan",
    "Carlos",
    "Luis",
    "Pedro",
    "Miguel",
    "Ana",
    "María",
    "Lucía",
    "Carla",
    "Paola",
    "Jorge",
    "Andrés",
    "Sofía",
    "Camila",
    "Valentina",
    "Daniel",
    "Fernando",
    "Rosa",
    "Carmen",
    "Julia",
    "Gabriel",
    "Sebastián",
    "Alejandro",
    "Ignacio",
    "Diego",
]

APELLIDOS = [
    "Quispe",
    "Huamán",
    "García",
    "Torres",
    "Flores",
    "Ramírez",
    "Sánchez",
    "Vargas",
    "Rojas",
    "Medina",
    "Castro",
    "López",
    "Gómez",
    "Reyes",
    "Navarro",
    "Mendoza",
    "Paredes",
    "Valverde",
    "Salazar",
    "Cáceres",
]


def random_name():
    return f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"


# -----------------------------
# PERFILES USANDO SOLO NUMEROS
# -----------------------------
PROFILE_GOOD = {
    "study_hours_per_day": lambda: round(random.uniform(3.5, 7.0), 1),
    "social_media_hours": lambda: round(random.uniform(0.5, 3.0), 1),
    "netflix_hours": lambda: round(random.uniform(0.3, 2.0), 1),
    "attendance_percentage": lambda: round(random.uniform(80, 100), 1),
    "sleep_hours": lambda: round(random.uniform(6.0, 8.0), 1),
    "exercise_frequency": lambda: round(random.uniform(3, 5), 1),
    "mental_health_rating": lambda: round(random.uniform(6, 9), 1),
    "academic_motivation": lambda: round(random.uniform(6, 9), 1),
    "time_management": lambda: round(random.uniform(3, 5), 1),
    "procrastination_level": lambda: round(random.uniform(1, 3), 1),
    "focus_level": lambda: round(random.uniform(3.5, 5), 1),
    "test_anxiety_level": lambda: round(random.uniform(3, 6), 1),
    "academic_self_efficacy": lambda: round(random.uniform(6, 9), 1),
    "study_techniques_usage": lambda: round(random.uniform(3, 5), 1),
    "home_study_environment": lambda: round(random.uniform(3, 5), 1),
    "study_resources_availability": lambda: round(random.uniform(3, 5), 1),
    "financial_stress_level": lambda: round(random.uniform(1, 3), 1),
}

PROFILE_RISK = {
    "study_hours_per_day": lambda: round(random.uniform(0.5, 3.5), 1),
    "social_media_hours": lambda: round(random.uniform(2, 5), 1),
    "netflix_hours": lambda: round(random.uniform(1.0, 4.0), 1),
    "attendance_percentage": lambda: round(random.uniform(50, 85), 1),
    "sleep_hours": lambda: round(random.uniform(4.5, 7.0), 1),
    "exercise_frequency": lambda: round(random.uniform(1, 3), 1),
    "mental_health_rating": lambda: round(random.uniform(3, 6), 1),
    "academic_motivation": lambda: round(random.uniform(1, 4), 1),
    "time_management": lambda: round(random.uniform(1, 3), 1),
    "procrastination_level": lambda: round(random.uniform(3, 5), 1),
    "focus_level": lambda: round(random.uniform(1.5, 3), 1),
    "test_anxiety_level": lambda: round(random.uniform(5, 9), 1),
    "academic_self_efficacy": lambda: round(random.uniform(2, 5), 1),
    "study_techniques_usage": lambda: round(random.uniform(1, 3), 1),
    "home_study_environment": lambda: round(random.uniform(1, 3), 1),
    "study_resources_availability": lambda: round(random.uniform(1, 3), 1),
    "financial_stress_level": lambda: round(random.uniform(3, 5), 1),
}


def generate(profile):
    return {k: v() for k, v in profile.items()}


# ============================================================
# INSERTAR ESTUDIANTES (CON LOGS)
# ============================================================


def insert_students(tutor_id: int):
    db: Session = SessionLocal()
    print("\n===============================")
    print("📌 INSERTANDO ESTUDIANTES NUMÉRICOS")
    print("===============================\n")

    num_good = int(TOTAL * 0.40)
    num_risk = TOTAL - num_good

    print(f"Total a insertar: {TOTAL}")
    print(f" - Buenos: {num_good}")
    print(f" - Riesgo: {num_risk}\n")

    inserted = 0

    for i in range(num_good):
        values = generate(PROFILE_GOOD)
        nombre = random_name()
        print(f"[GOOD {i+1}/{num_good}] {nombre} → {values}")
        db.add(Student(nombre=nombre, tutor_id=tutor_id, **values))
        inserted += 1

    for i in range(num_risk):
        values = generate(PROFILE_RISK)
        nombre = random_name()
        print(f"[RISK {i+1}/{num_risk}] {nombre} → {values}")
        db.add(Student(nombre=nombre, tutor_id=tutor_id, **values))
        inserted += 1

    db.commit()
    print("\n✔ COMMIT realizado correctamente.")
    print(f"🏁 FINALIZADO → {inserted}/{TOTAL} estudiantes insertados\n")


# ============================================================
# EJECUCIÓN DIRECTA DEL SCRIPT
# ============================================================
if __name__ == "__main__":
    print("\n===============================")
    print("🚀 Ejecutando seeder de estudiantes...")
    print("===============================\n")

    TUTOR_ID = 1  # <-- AJUSTA AQUÍ

    insert_students(TUTOR_ID)

    print("\n✔ Seeder finalizado sin errores.\n")
