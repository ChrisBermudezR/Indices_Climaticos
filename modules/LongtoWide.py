"""
longtowide.py
=================

Este módulo contiene funciones necesarias para procesar los datos en formato long que vienen de las fientes de datos de la NOAA.

https://www.cpc.ncep.noaa.gov/data/indices/

Descripción:
------------


Parámetros de entrada:
----------------------


Parámetros de salida:
---------------------


Librerías requeridas:
---------------------
- `pandas >=  1.5.3`
- `numpy >= 1.24.3`

Notas:
------


Autor:
------
Christian Bermúdez Rivas

Versión:
--------
1.0

Fecha de creación:
------------------
1 de noviembre de 2024
"""

import pandas as pd


def longtowide(path):
    pass

    data = pd.read_csv(path, sep=r"\s+", encoding='Utf-8')
    orden = ["DJF","JFM","FMA","MAM","AMJ","MJJ","JJA","JAS","ASO","SON","OND","NDJ"]
    data["SEAS"] = pd.Categorical(data["SEAS"], categories=orden, ordered=True)
    data = data.sort_values(["YR", "SEAS"])
    

    mes_central = {
        "DJF": "01",  # Ene
        "JFM": "02",  # Feb
        "FMA": "03",
        "MAM": "04",
        "AMJ": "05",
        "MJJ": "06",
        "JJA": "07",
        "JAS": "08",
        "ASO": "09",
        "SON": "10",
        "OND": "11",
        "NDJ": "12",
    }
    data["month"] = data["SEAS"].map(mes_central)
    # Nota: estaciones como NDJ/DJF abarcan dos años; dependiendo del análisis,
    # podrías ajustar YR para DJF/NDJ si quieres anclarlo a DIC o ENE.
    data["date"] = pd.to_datetime(dict(year=data["YR"], month=data["month"], day=15))
    

    data = data.rename(columns={
        "YR": "year"
    })


    data_filtrado = data[['year', 'month', 'ANOM']]
    

    wide = data_filtrado.pivot(index="year", columns="month", values="ANOM")
    wide.to_csv('./data/processed/roni.csv', index=True)
