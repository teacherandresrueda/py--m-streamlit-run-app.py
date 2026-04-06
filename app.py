import streamlit as st
from melate_sistema_total import generar_numeros

st.title("🎯 Melate AI - Sistema Inteligente")

if st.button("Generar combinación"):
    resultado = generar_numeros()
    st.success(f"Tu combinación: {resultado}")
    st.info("💡 Esta combinación está optimizada para evitar patrones comunes y repeticiones recientes.")
