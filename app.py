import streamlit as st
import random
import pandas as pd
from collections import Counter
from sklearn.linear_model import LogisticRegression

st.title("📊 AI Lottery Trading Dashboard")

uploaded_file = st.file_uploader("Upload your historical data", type=["csv","txt"])

RANGO = range(1,57)
historial = []

# =========================
# CARGAR DATOS
# =========================
if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    for linea in content.split("\n"):
        try:
            nums = list(map(int, linea.strip().split(",")))
            if len(nums) == 6:
                historial.append(nums)
        except:
            pass

st.write(f"Games loaded: {len(historial)}")

# =========================
# FRECUENCIA
# =========================
frecuencia = Counter()
for jugada in historial:
    frecuencia.update(jugada)

df_freq = pd.DataFrame(frecuencia.items(), columns=["Number","Frequency"])
df_freq = df_freq.sort_values(by="Frequency", ascending=False)

st.subheader("🔥 Frequency Ranking")
st.bar_chart(df_freq.set_index("Number"))

# =========================
# MACHINE LEARNING
# =========================
def preparar_datos(historial):
    X = []
    y = []

    for jugada in historial:
        vector = [0]*56
        for n in jugada:
            vector[n-1] = 1
        X.append(vector)

    for i in range(len(historial)):
        y.append(1)

    return X,y

if len(historial) > 5:
    X,y = preparar_datos(historial)
    model = LogisticRegression(max_iter=1000)
    model.fit(X,y)

    probabilidades = model.coef_[0]

    ml_scores = {i+1: abs(probabilidades[i]) for i in range(56)}

    df_ml = pd.DataFrame(ml_scores.items(), columns=["Number","Score"])
    df_ml = df_ml.sort_values(by="Score", ascending=False)

    st.subheader("🧠 ML Ranking")
    st.bar_chart(df_ml.set_index("Number"))

# =========================
# GENERADOR PRO
# =========================
def generar_combo():
    return sorted(random.sample(RANGO,6))

def score_combo(combo):
    score = 0
    score += sum(frecuencia.get(n,1) for n in combo)
    
    if len(historial) > 5:
        score += sum(ml_scores.get(n,0) for n in combo)

    return score

# =========================
# GENERAR
# =========================
if st.button("🚀 Generate PRO combinations"):

    resultados = []

    for _ in range(20000):
        combo = generar_combo()
        resultados.append(combo)

    resultados = list(set(tuple(c) for c in resultados))
    resultados = [list(c) for c in resultados]

    resultados_ordenados = sorted(resultados, key=score_combo, reverse=True)

    st.subheader("🏆 Best combinations")

    for c in resultados_ordenados[:10]:
        st.write(c, "Score:", score_combo(c))