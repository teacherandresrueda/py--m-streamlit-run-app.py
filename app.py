import streamlit as st
from melate_sistema_total import generar_numeros

st.title("Melate AI")

if st.button("Generar combinación"):
    resultado = generar_numeros()
    st.write(resultado)