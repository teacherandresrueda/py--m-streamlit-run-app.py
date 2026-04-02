import streamlit as st
import random
import pandas as pd
from collections import Counter
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Lottery PRO", layout="wide")
st.title("🔥 AI Lottery System PRO")

USER_FILE = "user_history.csv"
REAL_FILE = "real_results.csv"

# =========================
# ARCHIVOS
# =========================
if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["n1","n2","n3","n4","n5","n6"]).to_csv(USER_FILE, index=False)

if not os.path.exists(REAL_FILE):
    pd.DataFrame(columns=["n1","n2","n3","n4","n5","n6"]).to_csv(REAL_FILE, index=False)

user_df = pd.read_csv(USER_FILE)
real_df = pd.read_csv(REAL_FILE)

# =========================
# PARSE BLOQUES
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
# INPUTS
# =========================
st.subheader("📥 Tickets")

user_block = st.text_area("Ejemplo:\n1,2,3,4,5,6")

if st.button("Guardar tickets"):
    combos = parse_block(user_block)
    if combos:
        pd.DataFrame(combos, columns=user_df.columns).to_csv(USER_FILE, mode='a', header=False, index=False)
        st.success("Guardado")
    else:
        st.error("Formato inválido")

st.subheader("🌐 Resultados")

real_block = st.text_area("Ejemplo:\n1,2,3,4,5,6")

if st.button("Guardar resultados"):
    combos = parse_block(real_block)
    if combos:
        pd.DataFrame(combos, columns=real_df.columns).to_csv(REAL_FILE, mode='a', header=False, index=False)
        st.success("Guardado")
    else:
        st.error("Formato inválido")

# =========================
# FRECUENCIA
# =========================
def get_freq(df):
    nums = []
    for col in df.columns:
        nums += df[col].tolist()
    return Counter(nums)

freq_real = get_freq(real_df)
freq_user = get_freq(user_df)

# =========================
# SCORE
# =========================
def score_combo(combo):
    score = 0

    for n in combo:
        score += freq_real.get(n,0)

    # pares
    pares = sum(1 for n in combo if n % 2 == 0)
    if 2 <= pares <= 4:
        score += 5

    # evitar consecutivos
    for i in range(len(combo)-1):
        if combo[i+1] - combo[i] == 1:
            score -= 3

    return score

# =========================
# AUTO MODE
# =========================
def generar_auto():
    combos = []

    for _ in range(5000):
        c = sorted(random.sample(range(1,57),6))
        combos.append(c)

    combos = sorted(combos, key=score_combo, reverse=True)
    return combos[:3]

# =========================
# HIBRIDO
# =========================
def generar_hibrido():
    old_core = [7,12,22,31,38]
    new_core = [15,19,25,29,33]

    jugadas = []

    for _ in range(3):
        base = random.sample(old_core,3) + random.sample(new_core,2)

        candidatos = [n for n in range(1,57) if n not in base]
        candidatos = sorted(candidatos, key=lambda n: freq_real.get(n,0), reverse=True)

        jugadas.append(sorted(base + [candidatos[0]]))

    return jugadas

# =========================
# SMART MODE
# =========================
def detectar_estado():
    if len(real_df) < 6:
        return "estable"

    ultimos = set(real_df.tail(3).values.flatten())
    anteriores = set(real_df.tail(6).head(3).values.flatten())

    comunes = len(ultimos & anteriores)

    if comunes <= 3:
        return "cambio"
    elif comunes <= 6:
        return "transicion"
    else:
        return "estable"

# =========================
# DASH
# =========================
st.subheader("📊 Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Estado", detectar_estado())

with col2:
    top = sorted(freq_real.items(), key=lambda x: x[1], reverse=True)[:5]
    st.metric("Hot", [n for n,_ in top])

with col3:
    if st.button("🎯 Generar"):
        estado = detectar_estado()

        if estado == "cambio":
            jugadas = generar_hibrido()
        else:
            jugadas = generar_auto()

        st.subheader("🔥 TOP 3")
        for j in jugadas:
            st.write(j)

# =========================
# TEMPORAL
# =========================
st.subheader("📊 Temporal")

n = st.slider("Últimos sorteos",5,50,10)

df_temp = real_df.tail(n)
freq_temp = get_freq(df_temp)

df_chart = pd.DataFrame(freq_temp.items(), columns=["Number","Freq"])
df_chart = df_chart.sort_values(by="Freq", ascending=False)

st.bar_chart(df_chart.set_index("Number"))

# =========================
# MATCH
# =========================
st.subheader("🔍 Matches")

if not real_df.empty and not user_df.empty:
    ultimo = set(real_df.tail(1).values.flatten())

    for _, row in user_df.iterrows():
        ticket = set(row.tolist())
        match = ticket & ultimo

        if match:
            st.success(f"{list(ticket)} → {list(match)}")