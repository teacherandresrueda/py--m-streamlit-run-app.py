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

# =========================
# 🎨 ESTILO VISUAL PRO
# =========================
st.markdown("""
<style>
.block-green {
    background-color: #e8f5e9;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #2ecc71;
}
.block-red {
    background-color: #fdecea;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #e74c3c;
}
.block-yellow {
    background-color: #fff8e1;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #f1c40f;
}
.block-blue {
    background-color: #e3f2fd;
    padding: 15px;
    border-radius: 10px;
    border-left: 6px solid #3498db;
}
</style>
""", unsafe_allow_html=True)
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
# =========================
# ⚡ MODO HÍBRIDO
# =========================
st.subheader("⚡ Hybrid Mode")

old_core = [7,12,22,31,38]
new_core = [15,19,25,29,33]

def generar_hibrido(freq_real, freq_user):
    import random

    jugadas = []

    for _ in range(5):
        parte_vieja = random.sample(old_core, 3)
        parte_nueva = random.sample(new_core, 2)

        base = parte_vieja + parte_nueva

        candidatos = [n for n in range(1,57) if n not in base]

        def score(n):
            return freq_real.get(n,0)*2 + freq_user.get(n,0)

        candidatos = sorted(candidatos, key=score, reverse=True)

        sexto = candidatos[0]

        combo = sorted(base + [sexto])
        jugadas.append(combo)

    return jugadas

if st.button("🔥 Generar híbrido"):
    jugadas = generar_hibrido(real_df, user_df)

    for j in jugadas:
        st.write(j)
# =========================
# 🧠 MODO AUTOMÁTICO INTELIGENTE
# =========================
st.subheader("🧠 Smart Mode (auto decision)")

def detectar_ciclo_simple(real_df):
    if len(real_df) < 6:
        return "estable"

    ultimos = real_df.tail(3).values.flatten()
    anteriores = real_df.tail(6).head(3).values.flatten()

    comunes = len(set(ultimos) & set(anteriores))

    if comunes <= 3:
        return "cambio"
    elif comunes <= 6:
        return "transicion"
    else:
        return "estable"


if st.button("🧠 Ejecutar Smart Mode"):

    if real_df.empty:
        st.warning("Carga resultados primero")
    else:
        estado = detectar_ciclo_simple(real_df)

        st.write(f"Estado detectado: {estado}")

        if estado == "cambio":
            st.error("🔴 Cambio de ciclo → usando HÍBRIDO")
            jugadas = generar_hibrido(real_df, user_df)[:3]

        elif estado == "transicion":
            st.warning("🟡 Transición → usando HÍBRIDO")
            jugadas = generar_hibrido(real_df, user_df)[:3]

        else:
            st.success("🟢 Estable → usando AUTOMÁTICO")
            _, jugadas = generar_auto(real_df, user_df)
            jugadas = jugadas[:3]

        st.subheader("🎯 Jugadas finales")
        for j in jugadas:
            st.write(j)
# =========================
# 📊 FILTRO TEMPORAL
# =========================
st.subheader("📊 Temporal Analysis")

n = st.slider("Ver últimos sorteos", 5, 50, 10)

df_temp = real_df.tail(n)

nums = []
for col in df_temp.columns:
    nums += df_temp[col].tolist()

freq_temp = Counter(nums)

df_temp_freq = pd.DataFrame(freq_temp.items(), columns=["Number","Freq"])
df_temp_freq = df_temp_freq.sort_values(by="Freq", ascending=False)

st.bar_chart(df_temp_freq.set_index("Number"))
# =========================
# 🔍 MATCH USER vs RESULT
# =========================
st.subheader("🔍 Match Analysis")

if not real_df.empty and not user_df.empty:

    ultimo_resultado = set(real_df.tail(1).values.flatten())

    coincidencias = []

    for _, row in user_df.iterrows():
        ticket = set(row.tolist())
        match = ticket & ultimo_resultado

        if match:
            coincidencias.append((list(ticket), list(match)))

    if coincidencias:
        for t, m in coincidencias:
            st.write(f"🎟️ {t} → ✅ {m}")
    else:
        st.write("❌ No hubo coincidencias")