import streamlit as st
import random
import pandas as pd
from collections import Counter
import os

st.set_page_config(page_title="AI Lottery System PRO", layout="wide")
st.title("AI Lottery Trading System PRO")

# =========================
# ARCHIVOS
# =========================
USER_FILE = "user_history.csv"
REAL_FILE = "real_results.csv"

if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["n1","n2","n3","n4","n5","n6"]).to_csv(USER_FILE, index=False)

if not os.path.exists(REAL_FILE):
    pd.DataFrame(columns=["n1","n2","n3","n4","n5","n6"]).to_csv(REAL_FILE, index=False)

user_df = pd.read_csv(USER_FILE)
real_df = pd.read_csv(REAL_FILE)

# =========================
# INPUT USUARIO
# =========================
st.subheader("📥 Your Ticket")
user_input = st.text_input("Enter 6 numbers separated by commas")

if st.button("Save my ticket"):
    try:
        nums = list(map(int, user_input.split(",")))
        if len(nums) == 6:
            df_new = pd.DataFrame([nums], columns=user_df.columns)
            df_new.to_csv(USER_FILE, mode='a', header=False, index=False)
            st.success("Saved!")
        else:
            st.error("Enter exactly 6 numbers")
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
            df_new = pd.DataFrame([nums], columns=real_df.columns)
            df_new.to_csv(REAL_FILE, mode='a', header=False, index=False)
            st.success("Saved!")
        else:
            st.error("Enter exactly 6 numbers")
    except:
        st.error("Invalid format")

# =========================
# ANALISIS FRECUENCIA
# =========================
st.subheader("📊 Hot Numbers Analysis")

all_numbers = []

for col in real_df.columns:
    all_numbers += real_df[col].dropna().tolist()

freq = Counter(all_numbers)

if freq:
    df_freq = pd.DataFrame(freq.items(), columns=["Number", "Frequency"])
    df_freq = df_freq.sort_values(by="Frequency", ascending=False)
    st.bar_chart(df_freq.set_index("Number"))

# =========================
# SCORE INTELIGENTE
# =========================
def score_combo(combo):
    score = 0

    # Frecuencia
    for num in combo:
        score += freq.get(num, 0)

    # Penalizar consecutivos
    for i in range(len(combo)-1):
        if combo[i+1] - combo[i] == 1:
            score -= 2

    # Balance pares/impares
    pares = sum(1 for n in combo if n % 2 == 0)
    if 2 <= pares <= 4:
        score += 3

    return score

# =========================
# GENERADOR
# =========================
def generar_combo():
    return sorted(random.sample(range(1,57),6))

st.subheader("🎯 Generate Smart Combinations")

if st.button("Generate PRO combinations"):
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
import streamlit as st
import random
import pandas as pd
from collections import Counter
import os

st.set_page_config(page_title="AI Lottery System PRO", layout="wide")
st.title("AI Lottery Trading System PRO")

# =========================
# ARCHIVOS
# =========================
USER_FILE = "user_history.csv"
REAL_FILE = "real_results.csv"

if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["n1","n2","n3","n4","n5","n6"]).to_csv(USER_FILE, index=False)

if not os.path.exists(REAL_FILE):
    pd.DataFrame(columns=["n1","n2","n3","n4","n5","n6"]).to_csv(REAL_FILE, index=False)

user_df = pd.read_csv(USER_FILE)
real_df = pd.read_csv(REAL_FILE)

# =========================
# INPUT USUARIO
# =========================
st.subheader("📥 Your Ticket")
user_input = st.text_input("Enter 6 numbers separated by commas")

if st.button("Save my ticket"):
    try:
        nums = list(map(int, user_input.split(",")))
        if len(nums) == 6:
            df_new = pd.DataFrame([nums], columns=user_df.columns)
            df_new.to_csv(USER_FILE, mode='a', header=False, index=False)
            st.success("Saved!")
        else:
            st.error("Enter exactly 6 numbers")
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
            df_new = pd.DataFrame([nums], columns=real_df.columns)
            df_new.to_csv(REAL_FILE, mode='a', header=False, index=False)
            st.success("Saved!")
        else:
            st.error("Enter exactly 6 numbers")
    except:
        st.error("Invalid format")

# =========================
# ANALISIS FRECUENCIA
# =========================
st.subheader("📊 Hot Numbers Analysis")

all_numbers = []

for col in real_df.columns:
    all_numbers += real_df[col].dropna().tolist()

freq = Counter(all_numbers)

if freq:
    df_freq = pd.DataFrame(freq.items(), columns=["Number", "Frequency"])
    df_freq = df_freq.sort_values(by="Frequency", ascending=False)
    st.bar_chart(df_freq.set_index("Number"))

# =========================
# SCORE INTELIGENTE
# =========================
def score_combo(combo):
    score = 0

    # Frecuencia
    for num in combo:
        score += freq.get(num, 0)

    # Penalizar consecutivos
    for i in range(len(combo)-1):
        if combo[i+1] - combo[i] == 1:
            score -= 2

    # Balance pares/impares
    pares = sum(1 for n in combo if n % 2 == 0)
    if 2 <= pares <= 4:
        score += 3

    return score

# =========================
# GENERADOR
# =========================
def generar_combo():
    return sorted(random.sample(range(1,57),6))

st.subheader("🎯 Generate Smart Combinations")

if st.button("Generate PRO combinations"):
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