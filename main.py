# -*- coding: utf-8 -*-
"""
@author: Christian Bermúdez-Rivas
Nombre del script: CreacionTablas.py
Fecha de creación: Created on Fri Nov  1 16:00:24 2024
Descripción: Este script tiene como propósito realizar el ETL de los índices 
climáticos para estudiar el ENSO
Versión: 1.0 
Parámetros de entrada:
- archivo .csv con los datos de cada índice

Parámetros de salida:
- archivos .csv para sesr enviados a la base de datos.

Librerías requeridas:
-  `pandas >= 1.2`).

Notas:
- Este script sólo está diseñado para el índice ONI y el índice IMT
"""
# Importar las librerías
import pandas as pd
import openpyxl
# from eventClassifier import oniClassifier #Módulo de clasificación de eventos para cada indice
from indexes import oniIndex, meiIndex

# Lectura del archivo de datos de los índices posterior a la estructuración
oni_entire_df = pd.read_csv("./data/oni_entire.csv")
mei_entire_df = pd.read_csv("./data/mei_entire.csv")

# Aplicación de las funciones de organización de la tabla final
oni_entire_df_long = oniIndex(oni_entire_df) ######
mei_entire_df_long = meiIndex(mei_entire_df) ######

tabla_total = pd.concat([oni_entire_df_long, mei_entire_df_long], axis=0)


# Exportación de l atabla final a csv y xlsx
tabla_total.to_excel("Indices_Total.xlsx", sheet_name="indices", index=False)
tabla_total.to_csv("Indices_Total.csv", index=False)
