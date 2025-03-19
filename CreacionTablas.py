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
# from eventClassifier import oniClassifier #Módulo de clasificación de eventos para cada indice
from indexes import oniIndex

# Lectura del archivo de datos de los índices posterior a la estructuración
oni_entire_df = pd.read_csv(".\data\oni_entire.csv")
# Aplicación de las funciones de organización de la tabla final
oni_entire_df_long = oniIndex(oni_entire_df) ######
# Exportación de l atabla final a csv y xlsx
oni_entire_df_long.to_excel("Indices_Total.xlsx", index=False, encoding='utf-8-sig')
oni_entire_df_long.to_csv("Indices_Total.csv", index=False, encoding='utf-8-sig')

# Lista de DataFrames
dataframes = [oni_entire_df_long]
            
 

# Concatenar por filas
df_long = pd.concat(dataframes, axis=0)



df_long = pd.read_excel("Indices_Total_Manual.xlsx")


####Normalizacion
#units
units = df_long[['unit']].drop_duplicates()
units['id'] = range(1, len(units) + 1)
units=units[['id', 'unit']]

#events
events =  df_long[['event', 'event_description']].drop_duplicates()
events['id'] = range(1, len(events) + 1)
events=events[['id', 'event', 'event_description']]

#date
dates = df_long[['date']].drop_duplicates()
dates['id'] = range(1, len(dates) + 1)
dates=dates[['id', 'date']]

"""
REVISAR LA lÖGICA DE ESTO QUE HA CAMBIADO LA RELACIÖN EN EL MODELO E-R
#phase
phases =  df_long[['phase', 'phase_description', 'event']]
phases = pd.merge(phases, events, on='event', how='left')
phases = phases.drop_duplicates()
phases = phases[['phase', 'phase_description', 'id']]
phases = phases.rename(columns = {'id': 'id_event'})
phases['id'] = range(1, len(phases) + 1)
phases=phases[['id', 'phase', 'phase_description', 'id_event']]
"""


#indexes
indexes = df_long[['index_name', 'index_description', 'unit']]
indexes = pd.merge(indexes, units, on='unit', how='left')
indexes = indexes.rename(columns = {'id' : 'id_unit'})
indexes = indexes.drop_duplicates()
indexes = indexes[['index_name', 'index_description', 'id_unit']]
indexes['id'] = range(1, len(indexes) + 1)
indexes = indexes[['id', 'index_name', 'index_description', 'id_unit']]

#indexes_values
indexes_values = df_long[['value', 'date', 'phase', 'index_name']]
indexes_values = pd.merge(indexes_values, indexes, on='index_name', how='left')
indexes_values = indexes_values.rename(columns = {'id' : 'id_index'})
indexes_values = indexes_values[['value', 'date', 'phase',  'id_index']]
indexes_values = pd.merge(indexes_values, dates, on='date', how='left')
indexes_values = indexes_values.rename(columns = { 'id' : 'id_date'})
indexes_values = indexes_values[['value',  'phase',  'id_index', 'id_date']]
indexes_values = pd.merge(indexes_values, phases, on='phase', how='left')
indexes_values = indexes_values.rename(columns = {'id' : 'id_phase'})
indexes_values = indexes_values[['value',  'id_phase',  'id_index', 'id_date']]
indexes_values['id'] = range(1, len(indexes_values) + 1)
indexes_values = indexes_values[['id','value',  'id_phase',  'id_index', 'id_date']]

#exportar archivos
units.to_csv("./base_datos/units.csv", index=False, encoding='UTF-8')
events.to_csv("./base_datos/events.csv", index=False, encoding='UTF-8')
dates.to_csv("./base_datos/dates.csv", index=False, encoding='UTF-8')
phases.to_csv("./base_datos/phases.csv", index=False, encoding='UTF-8')
indexes.to_csv("./base_datos/indexes.csv", index=False, encoding='UTF-8')
indexes_values.to_csv("./base_datos/indexes_values.csv", index=False, encoding='UTF-8')
