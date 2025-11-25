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
import indexes 

print("inicio procesamiento")
# Lectura del archivo de datos de los índices posterior a la estructuración
oni_entire_df = pd.read_csv("./data/oni_entire.csv")


mei_entire_df = pd.read_csv("./data/mei_entire.csv")


soi_entire_df = pd.read_csv("./data/soi.csv")


nino12_entire_df = pd.read_csv("./data/niño 1+2.csv")


nino3_entire_df = pd.read_csv("./data/niño 3.csv")


nino34_entire_df = pd.read_csv("./data/niño 3+4.csv")


nino4_entire_df = pd.read_csv("./data/niño 4.csv")

#IMT_entire_df = pd.read_csv("./data/IMT.csv")



# Aplicación de las funciones de organización de la tabla final
oni_entire_df_long = indexes.oniIndex(oni_entire_df) ######
oni_entire_df_long.dropna(subset=['value'], inplace=True)

mei_entire_df_long = indexes.meiIndex(mei_entire_df) ######
mei_entire_df_long.dropna(subset=['value'], inplace=True)

soi_entire_df_df_long = indexes.soiIndex(soi_entire_df) ######
soi_entire_df_df_long.dropna(subset=['value'], inplace=True)

nino12_entire_df_long = indexes.nino12Index(nino12_entire_df) ######
nino12_entire_df_long.dropna(subset=['value'], inplace=True)

nino3_entire_df_long = indexes.nino3Index(nino3_entire_df) ######
nino3_entire_df_long.dropna(subset=['value'], inplace=True)

nino34_entire_df_long = indexes.nino34Index(nino34_entire_df) ######
nino34_entire_df_long.dropna(subset=['value'], inplace=True)

nino4_entire_df_long = indexes.nino4Index(nino4_entire_df) ######
nino4_entire_df_long.dropna(subset=['value'], inplace=True)

#IMT_entire_df_long = indexes.IMTIndex(IMT_entire_df) ######
#IMT_entire_df_long.dropna(subset=['value'], inplace=True)

tabla_total = pd.concat([
                            oni_entire_df_long, 
                            nino12_entire_df_long,
                            nino3_entire_df_long,
                            nino34_entire_df_long,
                            nino4_entire_df_long,
                            soi_entire_df_df_long,
                            mei_entire_df_long                         
                         ], axis=0)


# Exportación de l atabla final a csv y xlsx
print("exportando los datos")
tabla_total.to_excel("Indices_Total.xlsx", sheet_name="indices", index=False)
tabla_total.to_csv("Indices_Total.csv", index=False)
