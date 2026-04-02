import streamlit as st
import random
from collections import Counter

st.title(🤖 Number AI ELITE)

st.markdown(### 📂 Upload your historical results)

uploaded_file = st.file_uploader(Upload CSV or TXT, type=[csv, txt])

RANGO = range(1, 57)

historial = []

# 📥 CARGA DE ARCHIVO
if uploaded_file
    content = uploaded_file.read().decode(utf-8)
    lineas = content.split(n)
    
    for linea in lineas
        try
            nums = list(map(int, linea.strip().split(,)))
            if len(nums) == 6
                historial.append(nums)
        except
            pass

st.write(fLoaded games {len(historial)})

# 📊 ANÁLISIS
def calcular_frecuencia(historial)
    contador = Counter()
    for jugada in historial
        contador.update(jugada)
    return contador

frecuencia = calcular_frecuencia(historial)

# 🔥 HOT & COLD
hot = frecuencia.most_common(10)
cold = sorted(frecuencia.items(), key=lambda x x[1])[10]

st.subheader(🔥 Hot numbers)
st.write(hot)

st.subheader(❄️ Cold numbers)
st.write(cold)

# ⚖️ BALANCE
def evaluar_balance(combo)
    pares = sum(1 for n in combo if n % 2 == 0)
    bajos = sum(1 for n in combo if n = 28)
    return (2 = pares = 4) and (2 = bajos = 4)

# 🧠 SIMILITUD
def similitud(c1, c2)
    return len(set(c1) & set(c2))

def evitar_repetidos(combo, historial)
    for h in historial
        if similitud(combo, h) = 4
            return False
    return True

# 🎯 SCORE INTELIGENTE
def score_combo(combo)
    score = 0
    score += sum(frecuencia.get(n, 1) for n in combo)
    
    if evaluar_balance(combo)
        score += 10
    
    # bonus por incluir números calientes
    score += sum(3 for n, _ in hot if n in combo)
    
    return score

# 🚀 GENERACIÓN
if st.button(🚀 Generate Elite Combinations)
    
    resultados = []

    for _ in range(15000)
        combo = sorted(random.sample(RANGO, 6))
        
        if evaluar_balance(combo) and evitar_repetidos(combo, historial)
            resultados.append(combo)

    resultados = list(set(tuple(c) for c in resultados))
    resultados = [list(c) for c in resultados]

    resultados_ordenados = sorted(resultados, key=score_combo, reverse=True)

    st.subheader(🏆 Best combinations based on your history)

    for c in resultados_ordenados[10]
        st.write(c, Score, score_combo(c))