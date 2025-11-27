def map_study_hours(v):
    if v < 3.5:
        return "Cortas"
    if v < 5.5:
        return "Adecuadas"
    return "Intensas"


def map_social_media(v):
    if v < 1:
        return "Ligero"
    if v < 2:
        return "Moderado"
    return "Excesivo"


def map_netflix(v):
    if v < 1:
        return "Poco"
    if v < 2:
        return "Media"
    return "Alta"


def map_attendance(v):
    if v < 80:
        return "Irregular"
    if v < 95:
        return "Regular"
    return "Constante"


def map_sleep(v):
    if v < 6.5:
        return "Insuficiente"
    if v < 8:
        return "Normal"
    return "Extendido"


def map_exercise(v):
    if v < 3.5:
        return "Sedentario"
    if v < 4.5:
        return "Activo"
    return "Frecuente"


def map_mental_health(v):
    if v < 6.5:
        return "Delicada"
    if v < 8:
        return "Estable"
    return "Optima"


def map_anxiety(v):
    if v < 4:
        return "Leve"
    if v < 6:
        return "Moderada"
    return "Severa"


def map_financial_stress(v):
    if v < 2:
        return "Bajo_Estres"
    if v < 3:
        return "Medio_Estres"
    return "Alto_Estres"


def map_focus(v):
    if v < 4:
        return "Disperso"
    return "Concentrado"


def map_motivation(v):
    if v < 6:
        return "Limitada"
    if v < 8:
        return "Media"
    return "Alta"


def map_self_efficacy(v):
    if v < 7:
        return "Confiado"
    return "Muy_Confiado"


def map_time_management(v):
    if v < 3.5:
        return "Caotico"
    if v < 4.5:
        return "Intermedio"
    return "Adecuado"


def map_study_techniques(v):
    if v < 3.5:
        return "Basic"
    if v < 4.5:
        return "Intermed"
    return "Avanzado"


def map_resources(v):
    if v < 3.5:
        return "Escasos"
    if v < 4.5:
        return "Suficientes"
    return "Abundantes"
