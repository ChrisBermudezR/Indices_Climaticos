# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 18:57:49 2024

@author: CBermudezr
"""

#migración

import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os

# Conectar a la base de datos de PostgreSQL
# Reemplaza los valores con tus propios datos de conexión
engine = create_engine('postgresql+psycopg2://postgres:ADMIN@localhost:5432/indexes')


# Ruta de la carpeta con archivos CSV
ruta_carpeta = './base_datos/'

for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith('.csv'):
        # Leer cada archivo CSV
        df = pd.read_csv(os.path.join(ruta_carpeta, archivo))
        
        # Guardar en PostgreSQL usando el nombre del archivo como nombre de la tabla (sin extensión)
        nombre_tabla = os.path.splitext(archivo)[0]
        df.to_sql(nombre_tabla, engine, index=False, if_exists='replace')

print("Migración de múltiples archivos completada con éxito.")




# Ejecutar el join y cargar los datos en un DataFrame
query = """
SELECT 
    iv.id AS indexes_values_id,
    iv.value,
    iv.id_date,
    iv.id_phase,
    iv.id_index,
    i.index_name,
    i.index_description,
    i.id_unit
FROM 
    indexes_values iv
JOIN 
    indexes i ON iv.id_index = i.id;
"""

df = pd.read_sql(query, engine)

# Mostrar el DataFrame
print(df)
