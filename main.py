import json
from datetime import date

RUTA_COMIDAS = "data/comidas.json"
RUTA_HISTORIAL = "data/historial.json"

#funcion que carga las comidas del archivo .json
#quizas actualizar por si aparece otra comida????
def cargar_comidas(ruta):
    with open(ruta, "r", encoding = "utf-8") as f:
        comidas = json.load(f)
        return comidas

#funcion que carga el historial del archivo .json
def cargar_historial(ruta):
    with open(ruta, "r", encoding = "utf-8") as f:
        historial = json.load(f)
        return historial

#funcion que actualiza el historial del archivo .json
def actualizar_historial(ruta,historial):
    with open(ruta,"w", encoding="utf-8") as f:
        json.dump(historial,f,ensure_ascii=False, indent=2)

#funcion que imprime por pantalla la información sobre una comida
def imprimir_comida(comida):
    atributos = ["nombre","momento","saciedad","tiempo","esfuerzo","gusto"]
    for clave in atributos:
        print(clave.capitalize() + ":", comida[clave])
    print()


def viola_regla_dias(comida, historial, fecha_actual_str, dias_minimos):
    ultima_fecha_str = None

    # 1. Buscar la última fecha de esa comida en el historial
    for entrada in historial:
        if entrada["nombre_comida"] == comida["nombre"]:
            ultima_fecha_str = entrada["fecha"]

    # 2. Si nunca se ha comido (no hay fecha), no viola la regla
    if ultima_fecha_str is None:
        return False

    # 3. Convertir strings a objetos date (YYYY-MM-DD)
    fecha_actual = date.fromisoformat(fecha_actual_str)
    fecha_ultima = date.fromisoformat(ultima_fecha_str)

    # 4. Calcular diferencia en días
    diff = fecha_actual - fecha_ultima
    dias_pasados = diff.days

    # 5. Decidir si viola la regla
    if dias_pasados < dias_minimos:
        return True   # está demasiado reciente
    else:
        return False  # han pasado suficientes días
    


#aqui cargo todos los datos necesarios
comidas = cargar_comidas(RUTA_COMIDAS)
historial = cargar_historial(RUTA_HISTORIAL)

#preguntas al usuario
momento_dia = str(int("Cual es el momento del día: "))
hambre = int(input("¿Cuánta hambre tienes?: "))
cansancio = int(input("¿Cuánto cansancio tienes?: "))
rapidez = int(input("¿Cómo de rápido quieres cocinar?: "))

candidatas = []

for comida in comidas:
    if comida.momento != momento_dia:
