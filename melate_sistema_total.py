import random
import json
import os
from collections import Counter

DATA_FILE = "historial_melate.json"

# -------------------------
# HISTORIAL
# -------------------------
def leer_historial():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_historial(nueva):
    historial = leer_historial()
    historial.append(nueva)
    with open(DATA_FILE, "w") as f:
        json.dump(historial, f)
def simulacion_montecarlo(n=10000):
    resultados = []

    for _ in range(n):
        jugada = sorted(random.sample(range(1,57), 6))
        resultados.extend(jugada)

    return analizar_frecuencia([resultados])
# -------------------------
# ANÁLISIS
# -------------------------
def analizar_frecuencia(historial):
    flat = [n for jugada in historial for n in jugada]
    return Counter(flat)

# -------------------------
# SCORE INTELIGENTE
# -------------------------
def score_numero(n, frecuencia):
    freq = frecuencia.get(n, 0)

    score = 0

    # penalizar muy repetidos
    score -= freq * 0.3

    # bonus zona media
    if 15 <= n <= 45:
        score += 2

    # evitar extremos
    if n < 5 or n > 52:
        score -= 1

    return score

# -------------------------
# VALIDACIONES
# -------------------------
def es_valida(comb):
    # evitar consecutivos largos
    consecutivos = sum(1 for i in range(len(comb)-1) if comb[i]+1 == comb[i+1])
    if consecutivos >= 3:
        return False

    # balance par/impar
    pares = sum(1 for n in comb if n % 2 == 0)
    if pares < 2 or pares > 4:
        return False

    # balance alto/bajo
    bajos = sum(1 for n in comb if n <= 28)
    if bajos < 2 or bajos > 4:
        return False

    return True

# -------------------------
# GENERADOR PRO
# -------------------------
def generar_numeros():
    historial = leer_historial()
    frecuencia = analizar_frecuencia(historial)

    intentos = 0

    while True:
        intentos += 1

        # generar candidatos con score
        candidatos = list(range(1, 57))
        candidatos.sort(key=lambda x: score_numero(x, frecuencia), reverse=True)

        seleccion = sorted(random.sample(candidatos[:30], 6))

        # evitar repetir jugadas recientes
        if seleccion in historial[-20:]:
            continue

        if es_valida(seleccion):
            guardar_historial(seleccion)
            return seleccion

        if intentos > 100:
            # fallback
            seleccion = sorted(random.sample(range(1, 57), 6))
            guardar_historial(seleccion)
            return seleccion
