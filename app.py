import streamlit as st
from melate_sistema_total import generar_numeros, leer_historial, analizar_frecuencia

st.set_page_config(page_title="Melate AI Pro", layout="centered")

st.title("🎯 Melate AI - Sistema Inteligente PRO")

# -------------------------
# GENERAR COMBINACIÓN
# -------------------------
if st.button("🔮 Generar combinación"):
    resultado = generar_numeros()
    st.success(f"Tu combinación: {resultado}")
    st.info("💡 Optimizada con historial y patrones dinámicos")

# -------------------------
# HISTORIAL
# -------------------------
st.subheader("📊 Historial acumulado")
historial = leer_historial()

if historial:
    st.write(historial)
else:
    st.warning("Aún no hay datos")

# -------------------------
# ANÁLISIS
# -------------------------
st.subheader("🧠 Análisis de frecuencia")

if historial:
    frecuencia = analizar_frecuencia(historial)

    # ordenar
    ordenados = sorted(frecuencia.items(), key=lambda x: x[1], reverse=True)

    # TOP calientes
    st.markdown("🔥 Números calientes")
    st.write(ordenados[:10])

    # FRÍOS
    st.markdown("❄️ Números fríos")
    st.write(ordenados[-10:])

    # gráfica
    st.bar_chart(frecuencia)

# -------------------------
# RESET
# -------------------------
if st.button("⚠️ Resetear historial"):
    with open("historial_melate.json", "w") as f:
        f.write("[]")
    st.warning("Historial reiniciado")
