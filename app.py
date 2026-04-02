import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Mind System", layout="centered")

st.title("🧠 Mind & Decision System")

DATA_FILE = "data.csv"
THOUGHT_FILE = "thoughts.csv"

# =========================
# CREAR ARCHIVOS
# =========================
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["fecha","dinero","horas","energia"]).to_csv(DATA_FILE, index=False)

if not os.path.exists(THOUGHT_FILE):
    pd.DataFrame(columns=["fecha","pensamiento"]).to_csv(THOUGHT_FILE, index=False)

df = pd.read_csv(DATA_FILE)
thoughts_df = pd.read_csv(THOUGHT_FILE)

# =========================
# 🟢 REGISTRO DIARIO
# =========================
st.header("📥 Registro Diario")

fecha = datetime.now().strftime("%Y-%m-%d")

dinero = st.number_input("💰 Dinero ganado", min_value=0)
horas = st.number_input("⏱️ Horas trabajadas", min_value=0.0)
energia = st.slider("⚡ Energía (1-5)", 1, 5)

if st.button("Guardar Día"):
    new_data = pd.DataFrame([[fecha, dinero, horas, energia]],
                            columns=["fecha","dinero","horas","energia"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Día guardado ✅")

# =========================
# 🧠 GESTOR DE PENSAMIENTO
# =========================
st.header("🧠 Descarga Mental")

pensamiento = st.text_area("Escribe lo que tienes en la cabeza...")

if st.button("Liberar Pensamiento"):
    new_thought = pd.DataFrame([[fecha, pensamiento]],
                               columns=["fecha","pensamiento"])
    thoughts_df = pd.concat([thoughts_df, new_thought], ignore_index=True)
    thoughts_df.to_csv(THOUGHT_FILE, index=False)
    st.success("Pensamiento liberado ✅")

# =========================
# 📊 ANÁLISIS
# =========================
st.header("📊 Análisis")

if not df.empty:
    st.subheader("Promedios")
    st.write(df[["dinero","horas","energia"]].mean())

    st.subheader("Mejor y peor día")
    st.write(f"🔥 Mejor ingreso: {df['dinero'].max()}")
    st.write(f"⚠️ Peor ingreso: {df['dinero'].min()}")

    st.subheader("Dinero por nivel de energía")
    avg_energy = df.groupby("energia")["dinero"].mean()
    st.write(avg_energy)

# =========================
# 🎯 RECOMENDACIÓN
# =========================
st.header("🎯 Recomendación")

if not df.empty:
    avg_energy = df.groupby("energia")["dinero"].mean()
    best_energy = avg_energy.idxmax()

    st.success(f"👉 Tu mejor rendimiento es con energía: {best_energy}")

    if energia < best_energy:
        st.warning("⚠️ Hoy podrías rendir menos")
    else:
        st.success("🔥 Buen momento para trabajar")

# =========================
# 🔍 REFLEXIÓN SIMPLE
# =========================
st.header("🔍 Últimos Pensamientos")

if not thoughts_df.empty:
    st.write(thoughts_df.tail(5))