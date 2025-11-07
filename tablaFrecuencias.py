import json
import numpy as np
import pandas as pd

def cuartil(tabla, k, n, h):
    pos = k * n / 4
    fila = tabla[tabla['Frecuencia Acumulada'] >= pos].iloc[0]
    Li = fila['Limite Inferior']
    Fi_1 = tabla.loc[tabla.index < fila.name, 'Frecuencia Absoluta'].sum()
    fi = fila['Frecuencia Absoluta']
    Qk = Li + ((pos - Fi_1) / fi) * h
    return Qk


def lambda_handler(event, context):

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
    k = round(np.sqrt(n))
    h = round((rango / k), 6)

    # Crear clases
    bins = np.arange(minimo, minimo + (k + 1) * h, h)
    if bins[-1] <= maximo:
        bins = np.append(bins, bins[-1] + h)

    clases = pd.cut(datos, bins=bins, right=False, include_lowest=True)
    frecuencia = clases.value_counts().sort_index()

    tabla = pd.DataFrame({
        'Limite Inferior': [iv.left for iv in frecuencia.index],
        'Limite Superior': [iv.right for iv in frecuencia.index],
        'Frecuencia Absoluta': frecuencia.values
    })

    tabla['Frecuencia Acumulada'] = tabla['Frecuencia Absoluta'].cumsum()
    tabla['FR'] = (tabla['Frecuencia Absoluta'] / n) * 100
    tabla['FR Acumulada'] = round(tabla['FR'].cumsum(), 2)
    tabla['mi'] = round((tabla['Limite Inferior'] + tabla['Limite Superior']) / 2, 2)
    tabla['mi*fi'] = round(tabla['mi'] * tabla['Frecuencia Absoluta'], 2)

    # Media agrupada
    media = (tabla['Frecuencia Absoluta'] * tabla['mi']).sum() / n

    # Mediana agrupada
    n_mediana = n / 2
    fila_mediana = tabla[tabla['Frecuencia Acumulada'] >= n_mediana].iloc[0]
    Li = fila_mediana['Limite Inferior']
    Fi_1 = tabla.loc[tabla.index < fila_mediana.name, 'Frecuencia Absoluta'].sum()
    fi = fila_mediana['Frecuencia Absoluta']
    mediana = Li + ((n_mediana - Fi_1) / fi) * h

    # Moda agrupada
    idx_moda = tabla['Frecuencia Absoluta'].idxmax()
    Li = tabla.loc[idx_moda, 'Limite Inferior']
    fi = tabla.loc[idx_moda, 'Frecuencia Absoluta']
    f_prev = tabla.loc[idx_moda - 1, 'Frecuencia Absoluta'] if idx_moda > 0 else 0
    f_next = tabla.loc[idx_moda + 1, 'Frecuencia Absoluta'] if idx_moda < len(tabla) - 1 else 0
    moda = Li + ((fi - f_prev) / ((2 * fi) - f_prev - f_next)) * h

    # Varianza y desviación
    tabla['(mi - media)^2'] = (tabla['mi'] - media) ** 2
    tabla['f*(mi - media)^2'] = tabla['Frecuencia Absoluta'] * tabla['(mi - media)^2']
    varianza = tabla['f*(mi - media)^2'].sum() / (n - 1)
    desviacion = np.sqrt(varianza)

    # Cuartiles
    Q1 = cuartil(tabla, 1, n, h)
    Q3 = cuartil(tabla, 3, n, h)
    IQR = Q3 - Q1

    # Media geométrica
    geom_media = np.exp(np.sum(tabla['Frecuencia Absoluta'] * np.log(tabla['mi'])) / n)

    # Construir respuesta JSON
    resultado = {
        "resumen": {
            "n": n,
            "minimo": minimo,
            "maximo": maximo,
            "rango": rango,
            "clases": k,
            "ancho_clase": h
        },
        "medidas": {
            "media": round(media, 2),
            "mediana": round(mediana, 2),
            "moda": round(moda, 2),
            "varianza": round(varianza, 2),
            "desviacion": round(desviacion, 2),
            "Q1": round(Q1, 2),
            "Q3": round(Q3, 2),
            "IQR": round(IQR, 2),
            "media_geometrica": round(geom_media, 2)
        },
        "tabla_frecuencias": tabla.round(2).to_dict(orient="records")
    }

    # Devolver formato compatible con API Gateway
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(resultado, ensure_ascii=False)
    }
