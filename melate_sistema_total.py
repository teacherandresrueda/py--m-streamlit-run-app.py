import random
import json
import os

DATA_FILE = "historial_melate.json"

def leer_historial():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def generar_numeros():
    historial = leer_historial()

    # aplanar historial
    flat = []
    for jugada in historial:
        for n in jugada:
            flat.append(n)

    # frecuencia simple
    frecuencia = {}
    for n in flat:
        frecuencia[n] = frecuencia.get(n, 0) + 1

    # candidatos
    candidatos = list(range(1, 57))

    # ordenar (menos repetidos primero)
    candidatos.sort(key=lambda x: frecuencia.get(x, 0))

    # generar combinación
    combinacion = sorted(random.sample(candidatos[:30], 6))

    # guardar
    historial.append(combinacion)
    with open(DATA_FILE, "w") as f:
        json.dump(historial, f)

    return combinacion
