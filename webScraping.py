# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 15:44:55 2024

@author: CBermudezr
"""



import os
import pandas as pd

# Ruta de la carpeta que contiene los archivos
folder_path = './data'

# Iterar sobre todos los archivos de la carpeta
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    
    # Verificar que sea un archivo
    if os.path.isfile(file_path):
        print(f"Procesando archivo: {file_name}")
        
        # Leer el archivo y mostrar las primeras líneas para analizar su contenido
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Mostrar las primeras líneas para verificar la estructura (opcional)
        # print(lines[:10])

        data = []

        for line in lines[1:]:
            columns = line.split()
            try:
                year = int(columns[0])  # Intentar convertir el primer valor a un entero (el año)
                values = [float(value) if value != '-99.9' else None for value in columns[1:]]  # Convertir valores, manejar datos faltantes
                data.append([year] + values)
            except ValueError:
                # Omitir cualquier línea que no comience con un año válido
                continue

        # Crear el DataFrame con los datos procesados
        columns = ['year', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        df = pd.DataFrame(data, columns=columns)

        # Guardar el DataFrame en un archivo CSV con el mismo nombre que el archivo original
        output_file = os.path.join(folder_path, f"{os.path.splitext(file_name)[0]}.csv")
        df.to_csv(output_file, sep=',', header=True, index=False)
        print(f"Archivo guardado: {output_file}")