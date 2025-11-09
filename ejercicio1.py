import numpy as np
import pandas as pd

# Datos de la tabla
limites_inferiores = [250.00, 260.00, 270.00, 280.00, 290.00, 300.00, 320.00]
limites_superiores = [259.99, 269.99, 279.99, 289.99, 299.99, 319.99, 379.99]
frecuencias = [8, 10, 16, 15, 10, 8, 3]

# Total de datos
n = sum(frecuencias)

# Crear DataFrame
tabla = pd.DataFrame({
    "Limite Inf.": limites_inferiores,
    "Limite Sup.": limites_superiores,
    "Frecuencia Absoluta": frecuencias
})

# Calcular columnas adicionales
tabla["Frecuencia Acumulada"] = tabla["Frecuencia Absoluta"].cumsum()
tabla["FR (%)"] = (tabla["Frecuencia Absoluta"] / n) * 100
tabla["FR Acumulada (%)"] = tabla["FR (%)"].cumsum()
tabla["mi"] = round((tabla["Limite Inf."] + tabla["Limite Sup."]) / 2, 2)
tabla["mi*fi"] = tabla["mi"] * tabla["Frecuencia Absoluta"]

# Ancho de clase (h)
rango = 379.99 - 250
h = round(tabla["Limite Sup."][0] - tabla["Limite Inf."][0] + 0.01, 2)  # +0.01 para redondeo

# Media
media = tabla["mi*fi"].sum() / n

# Mediana
n_mediana = n / 2
fila_mediana = tabla[tabla["Frecuencia Acumulada"] >= n_mediana].iloc[0]
Li = fila_mediana["Limite Inf."]
Fi_1 = tabla.loc[tabla.index < fila_mediana.name, "Frecuencia Absoluta"].sum()
fi = fila_mediana["Frecuencia Absoluta"]
mediana = Li + ((n_mediana - Fi_1) / fi) * h

# Moda
idx_moda = tabla["Frecuencia Absoluta"].idxmax()
Li = tabla.loc[idx_moda, "Limite Inf."]
fi = tabla.loc[idx_moda, "Frecuencia Absoluta"]
f_prev = tabla.loc[idx_moda - 1, "Frecuencia Absoluta"] if idx_moda > 0 else 0
f_next = tabla.loc[idx_moda + 1, "Frecuencia Absoluta"] if idx_moda < len(tabla) - 1 else 0
moda = Li + ((fi - f_prev) / ((2 * fi) - f_prev - f_next)) * h

# Varianza y desviación estándar
tabla["(mi - media)^2"] = (tabla["mi"] - media) ** 2
tabla["f*(mi - media)^2"] = tabla["Frecuencia Absoluta"] * tabla["(mi - media)^2"]
varianza = tabla["f*(mi - media)^2"].sum() / (n - 1)
desviacion = np.sqrt(varianza)

# Cuartiles e IQR
def cuartil(tabla, k, n, h):
    pos = k * n / 4
    fila = tabla[tabla["Frecuencia Acumulada"] >= pos].iloc[0]
    Li = fila["Limite Inf."]
    Fi_1 = tabla.loc[tabla.index < fila.name, "Frecuencia Absoluta"].sum()
    fi = fila["Frecuencia Absoluta"]
    Qk = Li + ((pos - Fi_1) / fi) * h
    return Qk

Q1 = cuartil(tabla, 1, n, h)
Q3 = cuartil(tabla, 3, n, h)
IQR = Q3 - Q1

# Media geométrica
pond_media= np.sum(tabla["mi*fi"]/n)
geom_media = np.exp(np.sum(tabla["Frecuencia Absoluta"] * np.log(tabla["mi"])) / n)

# Resultados
print("\nTabla de frecuencias agrupadas:\n")
print(tabla)
print("\n--- Resultados ---")
print("Rango:", rango)
print("Ancho de clase:", h)
print(f"Media: {media:.2f}")
print(f"Mediana: {mediana:.2f}")
print(f"Moda: {moda:.2f}")
print(f"Varianza: {varianza:.2f}")
print(f"Desviación estándar: {desviacion:.2f}")
print(f"Q1: {Q1:.2f}")
print(f"Q3: {Q3:.2f}")
print(f"IQR: {IQR:.2f}")
print(f"Media ponderada: {pond_media:.2f}")
print(f"Media geométrica: {geom_media:.2f}")
