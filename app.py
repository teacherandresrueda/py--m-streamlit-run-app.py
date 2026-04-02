import streamlit as st
import random
import pandas as pd
from collections import Counter
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Lottery System PRO", layout="wide")
st.title("🔥 AI Lottery Trading System PRO")

USER_FILE = "user_history.csv"
REAL_FILE = "real_results.csv"

# =========================
# CREAR ARCHIVOS SI NO EXISTEN
# =========================
if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["n1","n2","n3","n4","n5","n6"]).to_csv(USER_FILE, index=False)

if not os.path.exists(REAL_FILE):
    pd.DataFrame(columns=["n1","n2","n3","n4","n5","n6"]).to_csv(REAL_FILE, index=False)

user_df = pd.read_csv(USER_FILE)
real_df = pd.read_csv(REAL_FILE)

# =========================
# FUNCION PARSE BLOQUES
# =========================
def parse_block(text):
    lines = text.strip().split("\n")
    valid = []

    for line in lines:
        try:
            nums = [int(x.strip()) for x in line.split(",")]
            if len(nums) == 6:
                valid.append(sorted(nums))
        except:
            continue

    return valid

# =========================
# INPUT USUARIO (BLOQUES)
# =========================
st.subheader("📥 Your Tickets (Paste blocks)")

user_block = st.text_area(
    "Example:\n1,2,3,4,5,6\n7,8,9,10,11,12",
    key="user_block"
)

if st.button("💾 Save my tickets"):
    combos = parse_block(user_block)

    if combos:
        df_new = pd.DataFrame(combos, columns=user_df.columns)
        df_new.to_csv(USER_FILE, mode='a', header=False, index=False)
        st.success(f"{len(combos)} tickets saved 🚀")
    else:
        st.error("Invalid format")

# =========================
# INPUT RESULTADOS
# =========================
st.subheader("🌐 Official Results (Paste blocks)")

real_block = st.text_area(
    "Example:\n1,2,3,4,5,6",
    key="real_block"
)

if st.button("💾 Save official results"):
    combos = parse_block(real_block)

    if combos:
        df_new = pd.DataFrame(combos, columns=real_df.columns)
        df_new.to_csv(REAL_FILE, mode='a', header=False, index=False)
        st.success(f"{len(combos)} results saved ✅")
    else:
        st.error("Invalid format")

# =========================
# ANALISIS DE FRECUENCIA
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
# ANALISIS DE PATRONES
# =========================
st.subheader("🧠 Pattern Analysis")

def analyze_patterns(df):
    pares_total = 0
    consecutivos_total = 0

    for _, row in df.iterrows():
        nums = sorted(row.tolist())

        pares_total += sum(1 for n in nums if n % 2 == 0)

        for i in range(len(nums)-1):
            if nums[i+1] - nums[i] == 1:
                consecutivos_total += 1

    return pares_total, consecutivos_total

if not real_df.empty:
    pares, consecutivos = analyze_patterns(real_df)

    st.write(f"🔢 Total even numbers: {pares}")
    st.write(f"🔗 Total consecutive patterns: {consecutivos}")

# =========================
# SCORE INTELIGENTE PRO
# =========================
def score_combo(combo):
    score = 0

    # Frecuencia
    for num in combo:
        score += freq.get(num, 0)

    # Penalizar consecutivos
    for i in range(len(combo)-1):
        if combo[i+1] - combo[i] == 1:
            score -= 3

    # Balance pares/impares
    pares = sum(1 for n in combo if n % 2 == 0)
    if 2 <= pares <= 4:
        score += 5

    # Distribución por rangos
    low = sum(1 for n in combo if n <= 28)
    high = sum(1 for n in combo if n > 28)
    if low >= 2 and high >= 2:
        score += 4

    return score

# =========================
# GENERADOR PRO
# =========================
def generar_combo():
    return sorted(random.sample(range(1,57),6))

st.subheader("🎯 Generate Smart Combinations")

if st.button("🚀 Generate PRO combinations"):

    resultados = []

    for _ in range(30000):
        combo = generar_combo()
        resultados.append(combo)

    resultados = list(set(tuple(c) for c in resultados))
    resultados = [list(c) for c in resultados]

    resultados_ordenados = sorted(resultados, key=score_combo, reverse=True)

    st.subheader("🏆 Top 10 Combinations")

    for c in resultados_ordenados[:10]:
        st.write(f"{c} → Score: {round(score_combo(c),2)}")
# =========================
# 🤖 MODO AUTOMÁTICO TOTAL
# =========================
st.subheader("🤖 Auto Mode (núcleo + jugadas)")

def detectar_nucleo(real_df, user_df, k=5):
    # Frecuencias combinadas (real pesa más)
    freq = {}
    for n in range(1,57):
        freq[n] = 0

    for col in real_df.columns:
        for v in real_df[col].dropna():
            freq[int(v)] += 2  # peso resultados

    for col in user_df.columns:
        for v in user_df[col].dropna():
            freq[int(v)] += 1  # peso usuario

    # Top k números
    ordenados = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    nucleo = sorted([n for n,_ in ordenados[:k]])
    return nucleo, freq


def elegir_sextos_auto(nucleo, freq):
    candidatos = [n for n in range(1,57) if n not in nucleo]

    def score(n):
        s = freq.get(n,0)

        # penalizar consecutivos con el núcleo
        for c in nucleo:
            if abs(n - c) == 1:
                s -= 3

        # preferencia zona media
        if 20 <= n <= 45:
            s += 2

        # evitar muy bajos
        if n < 5:
            s -= 2

        return s

    candidatos = sorted(candidatos, key=score, reverse=True)
    return candidatos[:5]


def generar_auto(real_df, user_df):
    nucleo, freq = detectar_nucleo(real_df, user_df, k=5)
    sextos = elegir_sextos_auto(nucleo, freq)

    jugadas = []
    for n in sextos:
        jugadas.append(sorted(nucleo + [n]))

    return nucleo, jugadas


if st.button("⚡ Generar automático"):
    if not real_df.empty:
        nucleo, jugadas = generar_auto(real_df, user_df)

        st.subheader("🧠 Núcleo detectado")
        st.write(nucleo)

        st.subheader("🎯 Jugadas recomendadas")
        for j in jugadas:
            st.write(j)
    else:
        st.warning("Carga resultados reales primero")