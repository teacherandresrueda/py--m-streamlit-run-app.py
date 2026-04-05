if uploaded_file:
    imagen = Image.open(uploaded_file)

    with st.spinner("Analizando..."):
        texto = extraer_texto(imagen)
        monto = extraer_monto(texto)
        fecha = extraer_fecha(texto)
        iva = extraer_iva(texto)
        metodo_pago = detectar_pago(texto)

        categoria = clasificar_gasto(texto)
        deduccion = evaluar_deduccion(categoria)
        recomendacion = generar_recomendacion(categoria)

st.set_page_config(page_title="Melate AI Sistema Total", layout="centered")
st.title("Melate AI - Sistema Total")

DATA_FILE = "historial_melate.json"

# -------------------------
# MEMORIA
# -------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# -------------------------
# INPUT
# -------------------------
st.subheader("Nuevo resultado")
new_input = st.text_input("Ejemplo: 5,12,23,34,45,56")

if st.button("Guardar resultado"):
    nums = [int(n) for n in new_input.split(",") if n.strip().isdigit()]
    if len(nums) >= 6:
        data.append(nums)
        save_data(data)
        st.success("Guardado")
    else:
        st.warning("Formato inválido")

# -------------------------
# FUNCIONES
# -------------------------
def weighted_freq(data):
    weights = Counter()
    for i, combo in enumerate(data):
        weight = i + 1
        for n in combo:
            weights[n] += weight
    return weights

def detect_core(data):
    counter = Counter()
    for combo in data:
        counter.update(set(combo))
    return [n for n, c in counter.items() if c >= 2]

def detect_almost_hits(data):
    freq = Counter([n for combo in data for n in combo])
    return [n for n, c in freq.items() if 2 <= c <= 3]

def detect_cycle(data):
    if len(data) < 3:
        return "insuficiente"

    last = set(data[-1])
    prev = set(data[-2])
    prev2 = set(data[-3])

    rep1 = len(last & prev)
    rep2 = len(prev & prev2)

    if rep1 >= 3 and rep2 >= 3:
        return "repeticion"
    elif 1 <= rep1 <= 2:
        return "transicion"
    else:
        return "ruptura"

def generate_by_cycle(cycle, core, top, cold, near):
    combo = []

    if cycle == "repeticion":
        combo.extend(random.sample(core, min(4, len(core))))
        combo.extend(random.sample(top, 2))

    elif cycle == "transicion":
        combo.extend(random.sample(core, min(2, len(core))))
        combo.extend(random.sample(top, 2))
        if near:
            combo.extend(random.sample(near, min(2, len(near))))

    elif cycle == "ruptura":
        combo.extend(random.sample(cold, min(3, len(cold))))
        combo.extend(random.sample(top, 2))
        if near:
            combo.append(random.choice(near))
def generar_numeros():
    return [5, 12, 23, 34, 41, 49]

    return sorted(set(combo))

def score_combo(combo, wf, core, near, cold):
    score = 0

    for n in combo:
        score += wf.get(n, 0) * 0.5
        if n in core:
            score += 5
        if n in near:
            score += 3
        if n in cold:
            score += 2

    even = sum(1 for n in combo if n % 2 == 0)
    if 2 <= even <= 4:
        score += 3

    return score

# -------------------------
# EJECUCIÓN
# -------------------------
if st.button("Simular 500 combinaciones"):

    if len(data) < 5:
        st.warning("Necesitas más datos")
    else:
        wf = weighted_freq(data)
        df = pd.DataFrame(wf.items(), columns=["Número", "Peso"])
        df = df.sort_values(by="Peso", ascending=False)

        st.subheader("Ranking")
        st.dataframe(df)

        top = df.head(15)["Número"].tolist()
        cold = df.tail(15)["Número"].tolist()
        core = detect_core(data)
        near = detect_almost_hits(data)
        cycle = detect_cycle(data)

        st.subheader("Ciclo actual")
        st.success(cycle.upper())

        results = []

        for _ in range(500):
            combo = generate_by_cycle(cycle, core, top, cold, near)
            score = score_combo(combo, wf, core, near, cold)
            results.append((combo, score))

        results = sorted(results, key=lambda x: x[1], reverse=True)

        st.subheader("Top 5 combinaciones")
        for i in range(5):
            st.write(f"{i+1}. {results[i][0]} → Score: {round(results[i][1],2)}")

        st.success(f"COMBINACIÓN FINAL: {results[0][0]}")