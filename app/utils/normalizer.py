# app/utils/normalizer.py

MAP_INPUT = {
    # Sueño
    "Insuficiente": "Insuficiente",
    "Normal": "Normal",
    # Horas de estudio
    "Cortas": "Cortas",
    "Adecuadas": "Adecuadas",
    "Intensas": "Intensas",
    # Asistencia
    "Irregular": "Irregular",
    "Regular": "Regular",
    "Constante": "Constante",
    # Redes sociales / entretenimiento
    "Ligero": "Ligero",
    "Moderado": "Moderado",
    "Excesivo": "Excesivo",
    "Poco": "Poco",
    # Ejercicio
    "Sedentario": "Sedentario",
    "Activo": "Activo",
    "Frecuente": "Frecuente",
    # Salud mental
    "Delicada": "Delicada",
    "Óptima": "Optima",
    "Optima": "Optima",
    # Motivación
    "Limitada": "Limitada",
    "Media": "Media",
    "Alta": "Alta",
    # Enfoque
    "Disperso": "Disperso",
    "Concentrado": "Concentrado",
    # Gestión del tiempo
    "Caótico": "Caotico",
    "Caotico": "Caotico",
    "Adecuado": "Adecuado",
    # Ansiedad
    "Leve": "Leve",
    "Moderada": "Moderada",
    "Severa": "Severa",
    # Autoeficacia
    "Confiado": "Confiado",
    "Muy_Confiado": "Muy_Confiado",
    "Poco_Confiado": "Poco_Confiado",
    # Técnicas de estudio
    "Básico": "Basico",
    "Basico": "Basico",
    "Intermedio": "Intermedio",
    "Avanzado": "Avanzado",
    # Recursos / Entorno
    "Escaso": "Escasos",
    "Escasos": "Escasos",
    "Suficientes": "Suficientes",
    # Estrés financiero
    "Alto": "Alto",
    "Medio": "Medio",
    "Bajo": "Bajo",
}


def normalize(data: dict):
    fixed = {}
    for k, v in data.items():
        fixed[k] = MAP_INPUT.get(v, v)
    return fixed
