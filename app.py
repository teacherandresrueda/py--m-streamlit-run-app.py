from collections import Counter
import random

# 👉 PEGA AQUÍ TUS JUGADAS
historial = [
    [7,12,20,21,37,49],
    [7,8,22,35,37,53],
    [7,12,22,31,33,38],
    [7,12,22,31,38,45],
    [7,12,22,27,31,38],
    [8,24,29,33,41,50],
    [3,16,23,28,36,37],
    [12,22,30,31,40,56]
]

# 🔥 Contar frecuencia
todos = [num for jugada in historial for num in jugada]
conteo = Counter(todos)

# 🔝 Números más frecuentes (núcleo)
frecuentes = [num for num, _ in conteo.most_common(10)]

# 🎯 Selección inteligente
nucleo = frecuentes[:3]
transicion = frecuentes[3:5]

# 🎲 Número aleatorio (salto)
todos_posibles = list(range(1,57))
restantes = list(set(todos_posibles) - set(frecuentes))
salto = random.choice(restantes)

# 🔥 Jugada final
jugada = sorted(nucleo + transicion + [salto])

print("Núcleo:", nucleo)
print("Transición:", transicion)
print("Salto:", salto)
print("Jugada sugerida:", jugada)
