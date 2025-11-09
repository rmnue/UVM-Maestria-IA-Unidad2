import numpy as np
import math
import pandas as pd

def cuartil(tabla, k, n, h):
    pos = k * n / 4
    fila = tabla[tabla['Frecuencia Acumulada'] >= pos].iloc[0]
    Li = fila['Limite Inferior']
    Fi_1 = tabla.loc[tabla.index < fila.name, 'Frecuencia Absoluta'].sum()
    fi = fila['Frecuencia Absoluta']
    Qk = Li + ((pos - Fi_1) / fi) * h
    return Qk

datos = [
68, 84, 75, 82, 68, 90, 62, 88, 76, 93,
73, 79, 88, 73, 60, 93, 71, 59, 85, 75,
61, 65, 75, 87, 74, 62, 95, 78, 63, 72,
66, 78, 82, 75, 94, 77, 69, 74, 68, 60,
96, 78, 89, 61, 75, 95, 60, 79, 83, 71,
79, 62, 67, 97, 78, 85, 76, 65, 71, 75,
65, 80, 73, 57, 88, 78, 62, 76, 53, 74,
86, 67, 73, 81, 72, 63, 76, 75, 85, 77
]

n = len(datos)
minimo = min(datos)
maximo = max(datos)
rango = maximo - minimo
k = math.floor(np.sqrt(n))
h = round((rango / k),6)                

print("n:", n)
print("Mínimo:", minimo)
print("Máximo:", maximo)
print("Rango:", rango)
print("Clases (k):", k)
print("Ancho de clase (h):", h)


bins = [minimo + i * h for i in range(k + 1)]

#print("Límites de clase:", bins)


clases = pd.cut(datos, bins=bins, right=True, include_lowest=True)

# Contar la frecuencia por clase
frecuencia = clases.value_counts().sort_index()

tabla = pd.DataFrame({
    #'Intervalo': frecuencia.index.astype(str),
    'Limite Inferior': [iv.left for iv in frecuencia.index],
    'Limite Superior': [iv.right for iv in frecuencia.index],
    'Frecuencia Absoluta': frecuencia.values
})


tabla['Frecuencia Acumulada'] = tabla['Frecuencia Absoluta'].cumsum()
tabla['FR'] = (tabla['Frecuencia Absoluta'] / n) * 100
tabla['FR Acumulada'] = round(tabla['FR'].cumsum(), 2)
tabla['mi'] = round((tabla['Limite Inferior'] + tabla['Limite Superior']) / 2, 2)
tabla['mi*fi'] = round((tabla['mi'] * tabla['Frecuencia Absoluta']), 2)




#Media
media = (tabla['Frecuencia Absoluta'] * tabla['mi']).sum() / n
print("Media agrupada:", round(media, 2))

#Mediana
n_mediana = n / 2

fila_mediana = tabla[tabla['Frecuencia Acumulada'] >= n_mediana].iloc[0]

Li = fila_mediana['Limite Inferior']
Fi_1 = tabla.loc[tabla.index < fila_mediana.name, 'Frecuencia Absoluta'].sum()
fi = fila_mediana['Frecuencia Absoluta']

mediana = Li + ((n_mediana - Fi_1) / fi) * h
print("Mediana agrupada:", round(mediana, 2))

#Moda
idx_moda = tabla['Frecuencia Absoluta'].idxmax()

Li = tabla.loc[idx_moda, 'Limite Inferior']
fi = tabla.loc[idx_moda, 'Frecuencia Absoluta']
f_prev = tabla.loc[idx_moda - 1, 'Frecuencia Absoluta'] if idx_moda > 0 else 0
f_next = tabla.loc[idx_moda + 1, 'Frecuencia Absoluta'] if idx_moda < len(tabla) - 1 else 0

moda = Li + ((fi - f_prev) / ((2 * fi) - f_prev - f_next)) * h
print("Moda agrupada:", round(moda, 2))

## Varianza y Desviación
tabla['(mi - media)^2'] = (tabla['mi'] - media) ** 2
tabla['f*(mi - media)^2'] = tabla['Frecuencia Absoluta'] * tabla['(mi - media)^2']

varianza = tabla['f*(mi - media)^2'].sum() / (n - 1)   # varianza muestral
desviacion = np.sqrt(varianza)

print("\nTabla de frecuencias agrupadas:\n")
print(tabla)

print("Media:", round(media, 2))
print("Varianza agrupada:", round(varianza, 2))
print("Desviación estándar agrupada:", round(desviacion, 2))


Q1 = cuartil(tabla, 1, n, h)
Q3 = cuartil(tabla, 3, n, h)
IQR = Q3 - Q1

print("Q1:", round(Q1, 2))
print("Q3:", round(Q3, 2))
print("Rango intercuartílico (IQR):", round(IQR, 2))

geom_media = np.exp(np.sum(tabla['Frecuencia Absoluta'] * np.log(tabla['mi'])) / n)
print("Media geométrica agrupada:", round(geom_media, 2))
