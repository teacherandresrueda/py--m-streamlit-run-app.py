import random

def leer_historial():
    numeros = []
    try:
        with open("historial.txt", "r") as f:
            for linea in f:
                fila = [int(x) for x in linea.strip().split(",")]
                numeros.extend(fila)
    except:
        pass
    return numeros

def analizar_frecuencia(numeros):
    frecuencia = {}
    for n in numeros:
        frecuencia[n] = frecuencia.get(n, 0) + 1
    return frecuencia

def generar_numeros():
    historial = leer_historial()
    frecuencia = analizar_frecuencia(historial)

    # ordenar por frecuencia (más repetidos)
    ordenados = sorted(frecuencia, key=frecuencia.get, reverse=True)

    # tomar top + random para balance
    top = ordenados[:15] if ordenados else list(range(1,57))

    combinacion = sorted(random.sample(top, 6))
    return combinacion