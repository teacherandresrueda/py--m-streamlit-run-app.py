import streamlit as st
import random
import pandas as pd
from collections import Counter
import os
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="AI Lottery System", layout="wide")

st.title("🧠 AI Lottery Trading System PRO")

# =========================
# ARCHIVOS
# =========================
USER_FILE = "user_history.csv"
REAL_FILE = "real_results.csv"

if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["n1","n2","n3","n4","n5","n6"]).to_csv(USER_FILE, index=False)

if not os.path.exists(REAL_FILE):
    pd.DataFrame(columns=["n1","n2","n3","n4","n5","n6"]).to_csv(REAL_FILE, index=False)

# =========================
# INPUT USUARIO
# =========================
st.subheader("📂 Your Tickets")

user_input = st.text_input("Enter your ticket")

if st.button("Save my ticket"):
    try:
        nums = list(map(int, user_input.split(",")))
        if len(nums) == 6:
            df = pd.read_csv(USER_FILE)
            df.loc[len(df)] = nums
            df.to_csv(USER_FILE, index=False)
            st.success("Saved!")
    except:
        st.error("Invalid format")

# =========================
# INPUT RESULTADOS
# =========================
st.subheader("🌐 Official Results")

real_input = st.text_input("Enter winning numbers")

if st.button("Save official result"):
    try:
        nums = list(map(int, real_input.split(",")))
        if len(nums) == 6:
            df = pd.read_csv(REAL_FILE)
            df.loc[len(df)] = nums
            df.to_csv(REAL_FILE, index=False)
            st.success("Saved!")
    except:
        st.error("Invalid format")

# =========================
# CARGAR DATOS
# =========================
user_df = pd.read_csv(USER_FILE)
real_df = pd.read_csv(REAL_FILE)

st.write("📊 Your tickets:", len(user_df))
st.write("🌐 Real results:", len(real_df))

# =========================
# FRECUENCIA
# =========================
def freq(df):
    c = Counter()
    for _, row in df.iterrows():
        c.update(row.values)
    return c

user_freq = freq(user_df)
real_freq = freq(real_df)

# =========================
# COMBINACIÓN
# =========================
combined_freq = {}

for i in range(1,57):
    combined_freq[i] = user_freq.get(i,0)*2 + real_freq.get(i,0)

df_comb = pd.DataFrame(combined_freq.items(), columns=["Number","Score"])
df_comb = df_comb.sort_values(by="Score", ascending=False)

st.subheader("📊 Combined Intelligence")
st.bar_chart(df_comb.set_index("Number"))

# =========================
# MACHINE LEARNING
# =========================
def preparar_datos(df):
    X = []
    y = []

    for _, row in df.iterrows():
        vector = [0]*56
        for n in row.values:
            vector[n-1] = 1
        X.append(vector)
        y.append(1)

    return X,y

ml_scores = {}

if len(real_df) > 5:
    X,y = preparar_datos(real_df)

    model = LogisticRegression(max_iter=1000)
    model.fit(X,y)

    coef = model.coef_[0]

    for i in range(56):
        ml_scores[i+1] = abs(coef[i])

    df_ml = pd.DataFrame(ml_scores.items(), columns=["Number","ML Score"])
    df_ml = df_ml.sort_values(by="ML Score", ascending=False)

    st.subheader("🧠 ML Ranking")
    st.bar_chart(df_ml.set_index("Number"))

# =========================
# GENERADOR PRO
# =========================
RANGO = range(1,57)

def generar_combo():
    return sorted(random.sample(RANGO,6))

def score_combo(combo):
    score = 0

    # frecuencia combinada
    score += sum(combined_freq.get(n,1) for n in combo)

    # ML
    score += sum(ml_scores.get(n,0) for n in combo)

    return score

# =========================
# GENERAR
# =========================
st.subheader("🎯 Generate Smart Combinations")

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
        st.write(c, "Score:", round(score_combo(c),2))