from step_1_create_tutor import create_tutor
from step_2_reset_tables import reset_tables
from step_3_load_students import insert_students
from step_4_generate_predictions import generate_all_predictions

print("🚀 INICIANDO PROCESO COMPLETO...")

tutor_id = create_tutor()
reset_tables()
insert_students(tutor_id)
generate_all_predictions()

print("🎉 TODO LISTO ✔")
