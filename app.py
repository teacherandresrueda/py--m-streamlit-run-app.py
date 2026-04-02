import streamlit as st
import random
from collections import Counter

# TÍTULO
st.title("🎯 Number AI Lab")

# AVISO LEGAL
st.warning("⚠️ This app is for entertainment and statistical purposes only.")

# RANGO DE NÚMEROS
RANGO = range(1, 57)

# INPUT DEL USUARIO
historial_input = st.text_area("Enter previous numbers (comma separated):")

def parse_historial(texto):
    try:
        nums = list(map(int, texto.split(",")))
        return [nums]
    except:
        return []

historial = parse_historial(historial_input)

# GENERAR COMBINACIÓN
def generar_combinacion():
    return sorted(random.sample(RANGO, 6))

# EVALUAR BALANCE
def evaluar_balance(combo):
    bajos = sum(1 for n in combo if n <= 15)
    medios = sum(1 for n in combo if 16 <= n <= 30)
    altos = sum(1 for n in combo if n >= 31)
    return (bajos == 2 and medios == 2 and altos == 2)

# FRECUENCIA
def calcular_frecuencia(historial):
    contador = Counter()
    for jugada in historial:
        contador.update(jugada)
    return contador

frecuencia = calcular_frecuencia(historial)

# SCORE
def score_combo(combo):
    return sum(frecuencia.get(n, 1) for n in combo)

# BOTÓN
if st.button("🚀 Generate combinations"):

    resultados = []

    for _ in range(5000):
        combo = generar_combinacion()

        if evaluar_balance(combo):
            resultados.append(combo)

    # Quitar duplicados
    resultados = list(set(tuple(c) for c in resultados))
    resultados = [list(c) for c in resultados]

    # Ordenar por score
    resultados_ordenados = sorted(resultados, key=score_combo, reverse=True)

    # MOSTRAR RESULTADOS
    st.subheader("🔥 Top combinations:")

    for c in resultados_ordenados[:10]:
        st.write(c, "Score:", score_combo(c))