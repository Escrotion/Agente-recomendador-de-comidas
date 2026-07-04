import json
from datetime import date

RUTA_COMIDAS = "data/comidas.json"
RUTA_HISTORIAL = "data/historial.json"
DIAS_MINIMOS = 3

# funcion que carga las comidas del archivo .json
# quizas actualizar por si aparece otra comida????
# "ruta" es la ruta donde se encuentra el listado de comidas
def cargar_comidas(ruta):
    with open(ruta, "r", encoding = "utf-8") as f:
        comidas = json.load(f)
        return comidas

# funcion que carga el historial del archivo .json
# "ruta" es la ruta donde se encuentra el historial
def cargar_historial(ruta):
    with open(ruta, "r", encoding = "utf-8") as f:
        historial = json.load(f)
        return historial

# funcion que actualiza el historial del archivo .json
# "ruta" es la ruta donde se encuentra el historial
# "historial" es el fichero con el historial de comidas
def actualizar_historial(ruta,historial):
    with open(ruta,"w", encoding="utf-8") as f:
        json.dump(historial,f,ensure_ascii=False, indent=2)

# funcion que imprime por pantalla la informacion relacionada con una comida
# "comida" es el diccionario del que se lee
def imprimir_comida(comida):
    atributos = ["nombre","saciedad","tiempo","esfuerzo","gusto"]
    for clave in atributos:
        print(clave.capitalize() + ":", comida[clave])
    print()

# funcion que valida si una comida viola la restricción de los dias minimos o no
# "comida" es el diccionario del que se lee
# "historial" es el fichero con el historial de comidas
# "fecha_actual_str" es la fecha del momento en el que se hace la consulta
# "dias_minimos" es el limite de duas que pueden pasar entre la misma comida
def viola_regla_dias(comida, historial, fecha_actual_str, dias_minimos):
    ultima_fecha_str = None

    # 1. Buscar la última fecha de esa comida en el historial
    for entrada in historial:
        if entrada["nombre_comida"] == comida["nombre"]:
            ultima_fecha_str = entrada["fecha"]
            break

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


# funcion que calcula el score de cada comida para elegir las mejores candidatas
# "comida" es el diccionario del que se lee
# "hambre" es un entero que indica el hambre que tiene el usuario
# "cansancio" es un entero que indica el cansancio que tiene el usuario
# "rapidez" es un entero que indica la rapidez que quiere el usuario
def calcula_score(comida, hambre, cansancio, rapidez):  
    p_saciedad = 3 - abs(hambre - comida["saciedad"])

    esfuerzo_deseado = 4 - cansancio
    p_esfuerzo = 3 - abs(esfuerzo_deseado - comida["esfuerzo"])

    tiempo_deseado = 4 - rapidez
    p_rapidez = 3 - abs(tiempo_deseado - comida["tiempo"])

    coef_gusto = 1 + comida["gusto"] / 10.0

    score_base = p_esfuerzo + p_rapidez + p_saciedad
    score_total = coef_gusto * score_base

    return score_total

# funcion que se encarga de la entrada de datos
# mensaje es el input
# maximo y minimo son los limites
def pedir_entero_en_rango(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"Por favor, introduce un número entre {minimo} y {maximo}.")
        except ValueError:
            print("Por favor, introduce un número válido.")

# aqui ya pasamos al main
def main():
    # cargo todos los datos necesarios
    comidas = cargar_comidas(RUTA_COMIDAS)
    historial = cargar_historial(RUTA_HISTORIAL)

    # Pedimos al usuario los datos de entrada
    momento_dia = str(input("Cual es el momento del día: "))
    hambre = pedir_entero_en_rango("¿Cuánta hambre tienes? (1-3): ",1,3)
    cansancio = pedir_entero_en_rango("¿Cuánto cansancio tienes? (1-3): ",1,3)
    rapidez = pedir_entero_en_rango("¿Cómo de rápido quieres cocinar? (1-3): ",1,3)

    fecha_hoy = str(input("Escriba la fecha del día de hoy (en formato 'YYYY-MM-DD'): "))

    candidatas = []

    # creo una lista con las comidas candidatas
    for comida in comidas:
        if comida["momento"] == momento_dia:
            if not viola_regla_dias(comida,historial,fecha_hoy,DIAS_MINIMOS):
                score_comida = calcula_score(comida,hambre,cansancio,rapidez)
                candidatas.append((comida,score_comida))
    # ahora manejamos el caso de la excepción de saltarse los días
    if len(candidatas) == 0:
        for comida in comidas:
            if comida["momento"] == momento_dia:
                score_comida = calcula_score(comida,hambre,cansancio,rapidez)
                candidatas.append((comida,score_comida))

    candidatas.sort(key = lambda x: x[1] , reverse = True)
    print("Este es el top 3 de las comidas que te recomiendo:")
    print()
    for i in range(min(3,len(candidatas))):
        print("Opción",i+1,":")
        imprimir_comida(candidatas[i][0])
    
    num_opciones = min(3,len(candidatas))
    opcion = pedir_entero_en_rango(f"Eliga una opción (1-{num_opciones}): ",1,num_opciones)
    opcion -= 1

    comida_elegida = candidatas[opcion][0]

    encontrada = False

    for entrada in historial:
        if entrada["nombre_comida"] == comida_elegida["nombre"] and not encontrada:
            entrada["fecha"] = fecha_hoy
            entrada["momento"] = comida_elegida["momento"]
            encontrada = True

    if not encontrada:
        nueva_entrada = {
            "nombre_comida": comida_elegida["nombre"],
            "fecha": fecha_hoy,
            "momento": comida_elegida["momento"]
        }
        historial.append(nueva_entrada)

    actualizar_historial(RUTA_HISTORIAL, historial)


if __name__ == "__main__":
    main()
