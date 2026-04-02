import streamlit as st
import random
from collections import Counter

st.title("🧠 Number AI GOD MODE")

st.markdown("### Upload your historical winning numbers")

uploaded_file = st.file_uploader("Upload CSV or TXT", type=["csv", "txt"])

RANGO = range(1, 57)
historial = []

# ========================
# CARGA DE DATOS
# ========================
if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    for linea in content.split("\n"):
        try:
            nums = list(map(int, linea.strip().split(",")))
            if len(nums) == 6:
                historial.append(nums)
        except:
            pass

st.write(f"📊 Games loaded: {len(historial)}")

# ========================
# ANÁLISIS
# ========================
frecuencia = Counter()
for jugada in historial:
    frecuencia.update(jugada)

# HOT / COLD
hot = frecuencia.most_common(10)
cold = sorted(frecuencia.items(), key=lambda x: x[1])[:10]

st.subheader("🔥 Hot Numbers")
st.write(hot)

st.subheader("❄️ Cold Numbers")
st.write(cold)

# ========================
# PATRONES
# ========================
pares = []
bajos = []

for jugada in historial:
    pares.append(sum(1 for n in jugada if n % 2 == 0))
    bajos.append(sum(1 for n in jugada if n <= 28))

if pares:
    st.subheader("⚖️ Pattern Analysis")
    st.write(f"Avg even numbers: {sum(pares)/len(pares):.2f}")
    st.write(f"Avg low numbers: {sum(bajos)/len(bajos):.2f}")

# ========================
# FUNCIONES
# ========================
def generar_combo():
    return sorted(random.sample(RANGO, 6))

def evaluar_balance(combo):
    pares = sum(1 for n in combo if n % 2 == 0)
    bajos = sum(1 for n in combo if n <= 28)
    return (2 <= pares <= 4) and (2 <= bajos <= 4)

def similitud(c1, c2):
    return len(set(c1) & set(c2))

def evitar_repetidos(combo):
    for h in historial:
        if similitud(combo, h) >= 4:
            return False
    return True

# ========================
# SCORE AVANZADO
# ========================
def score_combo(combo):
    score = 0

    # frecuencia
    score += sum(frecuencia.get(n, 1) for n in combo)

    # balance
    if evaluar_balance(combo):
        score += 15

    # bonus números calientes
    score += sum(5 for n, _ in hot if n in combo)

    # penalizar números fríos
    score -= sum(3 for n, _ in cold if n in combo)

    return score

# ========================
# GENERACIÓN INTELIGENTE
# ========================
if st.button("🚀 Generate GOD combinations"):

    resultados = []

    for _ in range(20000):
        combo = generar_combo()

        if evaluar_balance(combo) and evitar_repetidos(combo):
            resultados.append(combo)

    resultados = list(set(tuple(c) for c in resultados))
    resultados = [list(c) for c in resultados]

    resultados_ordenados = sorted(resultados, key=score_combo, reverse=True)

    st.subheader("🏆 Best Strategic Combinations")

    for c in resultados_ordenados[:10]:
        st.write(c, "Score:", score_combo(c))