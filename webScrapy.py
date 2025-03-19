import os
import pandas as pd

# Ruta de la carpeta que contiene los archivos
folder_path = './data'

# Iterar sobre todos los archivos de la carpeta
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)

    # Verificar que sea un archivo válido
    if os.path.isfile(file_path):
        print(f"Procesando archivo: {file_name}")

        # Leer el archivo y analizar su contenido
        with open(file_path, 'r') as file:
            lines = file.readlines()

        data = []
        
        for line in lines:
            # Limpiar la línea y verificar si está vacía
            line = line.strip()
            if not line or line.startswith("Nino") or "https://" in line:
                continue  # Ignorar encabezados o líneas vacías
            
            # Dividir la línea en columnas
            columns = line.split()
            
            # Verificar que haya al menos un año y algún valor asociado
            if len(columns) < 2:
                print(f"Ignorando línea inesperada: {line}")
                continue

            try:
                # Intentar convertir el primer valor en el año
                year = int(columns[0])
                # Convertir los valores restantes en flotantes, manejando datos faltantes (-99.9)
                values = [float(value) if value != '-99.9' else None for value in columns[1:]]
                data.append([year] + values)
            except ValueError:
                print(f"Ignorando línea con datos no válidos: {line}")
                continue
        
        # Verificar si hay datos antes de crear el DataFrame
        if not data:
            print(f"No se encontraron datos válidos en {file_name}")
            continue

        # Definir los nombres de las columnas dinámicamente según los datos detectados
        num_months = len(data[0]) - 1  # Número de columnas menos el año
        column_names = ['year'] + [f"{month:02d}" for month in range(1, num_months + 1)]

        # Crear el DataFrame con los datos procesados
        df = pd.DataFrame(data, columns=column_names)

        # Guardar el DataFrame en un archivo CSV con el mismo nombre que el archivo original
        output_file = os.path.join(folder_path, f"{os.path.splitext(file_name)[0]}.csv")
        df.to_csv(output_file, sep=',', header=True, index=False)

        print(f"Archivo guardado: {output_file}")
