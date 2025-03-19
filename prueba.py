# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 17:05:36 2024

@author: CBermudezr
"""

#Importar las librerías
import pandas as pd
import numpy as np
#from eventClassifier import oniClassifier #Módulo de clasificación de eventos para cada indice
from indexes import oniIndex


#Lectura del archivo de datos de los índices posterior a la estructuración
df=pd.read_csv(".\data\oni_entire.csv")


df_long = df.melt(id_vars=['year'], var_name='month', value_name='value')
df_long['year'] = df_long['year'].astype(str)
#initial_line = pd.DataFrame({'year': ['1949'], 'month': ['12'], 'value': [-0.5]})
#df_long = pd.concat([initial_line, df_long], ignore_index=True)

df_long['day'] = 1
df_long['day'] = df_long['day'].astype(str)

df_long = df_long[df_long['value'] != -99.9]
df_long['value'] = df_long['value'].round(1)

df_long['date'] = pd.to_datetime(df_long[['year', 'month', 'day']])
df_long['date'] = df_long['date'].dt.strftime('%Y-%m-%d')
df_long = df_long[['date', 'value']]
df_long = df_long.sort_values(by='date')
df_long['date'] = pd.to_datetime(df_long['date'])

df_long['index_name'] = 'ONI'
df_long['index_description'] = 'Índice Niño oceánico: Media móvil de 3 meses de las anomalías de la TSM ERSST.v5 en la región Niño 3.4 (5°N-5°S, 120°-170°W) Calculada a partir del ERSST V5 (en NOAA/CPC).'
df_long['unit'] = '°C'

 # Crear una nueva columna 'Phase' con condiciones basadas en los valores de 'value'
df_long['phase'] = df_long['value'].apply(lambda x: 'Fría' if x <= -0.5 else ('Cálida' if x >= 0.5 else 'Neutra'))
df_long['phase_description'] = df_long['value'].apply(lambda x: 'Esta fase se caracteriza porque las anomalías de TSM en la región 3.4 son inferiores a -0.5 °C' 
                                                 if x < -0.5 else ('Esta fase se caracteriza porque las anomalías de TSM en la región 3.4 son superiores a 0.5 °C' 
                                                                   if x > 0.5 else 'Esta fase se caracteriza porque las anomalías de TSM son inferiores a 0.5 °C y superiores a -0.5 °C'))

anio_inicio = 1950
anio_fin = df_long['date'].iloc[-1].year
final_month = df_long['date'].iloc[-1].month
total_meses = pd.date_range(start=f'{anio_inicio}-01-01', end=f'{anio_fin}-{final_month}-01', freq='MS')
vector_index = np.array(df_long['value']).flatten()
vector_index = vector_index[:len(total_meses)]

# Identificar periodos El Niño
pos_nino = np.where(vector_index >= 0.5)[0]
D = np.diff(np.concatenate(([0], np.diff(pos_nino) == 1, [0])))
pos_partida = np.where(D == 1)[0]
pos_llegada = np.where(D == -1)[0]+1
posiciones = np.vstack((pos_partida, pos_llegada))
resultado = np.diff(posiciones, axis=0)
posiciones_nino = np.where(resultado>= 5)[1]
meses_nino = []

for i in posiciones_nino:
    periodos = pos_nino[pos_partida[i]:pos_llegada[i]]
    meses_nino.extend(total_meses[periodos])
    
Nino = pd.to_datetime(meses_nino)
Nino_event = pd.DataFrame({'date': Nino, 'event': 'Niño'})

# Identificar periodos La Niña
pos_nina = np.where(vector_index <= -0.5)[0]
D = np.diff(np.concatenate(([0], np.diff(pos_nina) == 1, [0])))
pos_partida = np.where(D == 1)[0]
pos_llegada = np.where(D == -1)[0]+1
posiciones = np.vstack((pos_partida, pos_llegada))
resultado = np.diff(posiciones, axis=0)
posiciones_nina = np.where(resultado >= 5)[1]
meses_nina = []
                    
for i in posiciones_nina:
    periodos = pos_nina[pos_partida[i]:pos_llegada[i]]
    meses_nina.extend(total_meses[periodos])
    
Nina = pd.to_datetime(meses_nina)
Nina_event = pd.DataFrame({'date': Nina, 'event': 'Niña'})

# Identificar periodos Neutros
pos_neutro_1 = np.isin(total_meses, Nino)
pos_neutro_2 = np.isin(total_meses, Nina)
Neutro = total_meses[~(pos_neutro_1 | pos_neutro_2)]

Neutro = pd.to_datetime(Neutro)
Neutro_event = pd.DataFrame({'date': Neutro, 'event': 'Neutro'})

event_total = pd.concat([Nino_event, Nina_event, Neutro_event]).sort_values(by='date').reset_index(drop=True)






 # Unir los eventos con el DataFrame original
df_long = pd.merge(df_long, event_total, on='date')

df_long['event_description'] = df_long['event'].apply(lambda x: 'Este evento se caracteriza porque la fase fría persiste durante al menos 5 meses consecutivos' 
                                                 if x == 'Niña' 
                                                 else ('Este evento se caracteriza porque la fase cálida persiste durante al menos 5 meses consecutivos'
                                                       if x == 'Niño' 
                                                       else 'Condiciones neutras'))


def clasificar_valor(x):
    """
    Clasifica un valor numérico en una categoría basada en rangos.

    Args:
        x (float): El valor numérico a clasificar.

    Returns:
        str: La categoría en la que cae el valor.
    """
    if -0.5 < x < 0.5:
        return '0'
    elif 0.5 <= x < 1.0 or -1.0 < x <= -0.5:
        return '1'
    elif 1.0 <= x < 1.5 or -1.5 < x <= -1.0:
        return '2'
    elif 1.5 <= x < 2.0 or -2.0 < x <= -1.5:
        return '3'
    else:
        return '4'
    
def evaluar_columnas(df, col1, col2, nueva_col):

    """

    Evalúa dos columnas en un DataFrame y crea una nueva columna basada en las condiciones especificadas.


    Args:

        df (pd.DataFrame): El DataFrame que contiene las columnas a evaluar.

        col1 (str): Nombre de la primera columna.

        col2 (str): Nombre de la segunda columna.

        nueva_col (str): Nombre de la nueva columna a crear.


    Returns:

        pd.DataFrame: El DataFrame modificado con la nueva columna.

    """

    def aplicar_condiciones(row):

        if 'Neutro' in row[col1]:

            return '0'

        else:

            return clasificar_valor(row[col2])


    df[nueva_col] = df.apply(aplicar_condiciones, axis=1)

    return df


prueba = evaluar_columnas(df_long, 'event', 'value', 'type')


prueba2 = df_long['value'].apply(clasificar_valor)

prueba = pd.DataFrame(prueba)
prueba = prueba.rename(columns={'value': 'type'})

prueba = pd.concat([prueba.type, df_long.value], axis=1)

df_long.to_excel("Indices_Total2.xlsx", index=False, encoding='utf-8-sig')

prueba['type'].to_csv("vector_type.csv", index=False, encoding='utf-8-sig')





####

data = pd.DataFrame(prueba[['date','type']])


# Procesar los datos para identificar rangos y modificar valores
def process_vector(dataframe):
    # Convertir la columna de interés en una lista, ignorando el encabezado
    values = dataframe.iloc[0:, 1].astype(int).tolist()
    
    # Variables para almacenar los rangos y el nuevo vector modificado
    ranges = []
    modified_values = values[:]
    
    # Inicializar variables de control

    start_idx = None

    for i, val in enumerate(values):

        if val != 0 and start_idx is None:  # Inicio de un segmento

            start_idx = i

        elif val == 0 and start_idx is not None:  # Fin de un segmento

            end_idx = i - 1

            segment = values[start_idx:end_idx + 1]

            

            # Encontrar el valor más alto que se repita al menos 3 veces consecutivas

            max_value_with_condition = None

            for j in range(len(segment) - 2):

                if segment[j] == segment[j + 1] == segment[j + 2]:

                    max_value_with_condition = segment[j]

            

            # Si se encuentra un valor válido, modificar el segmento

            if max_value_with_condition is not None:

                ranges.append((start_idx, end_idx))

                for j in range(start_idx, end_idx + 1):

                    modified_values[j] = max_value_with_condition

            start_idx = None



    # Si el último segmento llega hasta el final del vector

    if start_idx is not None:

        end_idx = len(values) - 1

        segment = values[start_idx:end_idx + 1]

        max_value_with_condition = None

        for j in range(len(segment) - 2):

            if segment[j] == segment[j + 1] == segment[j + 2]:

                max_value_with_condition = segment[j]

        if max_value_with_condition is not None:

            ranges.append((start_idx, end_idx))

            for j in range(start_idx, end_idx + 1):

                modified_values[j] = max_value_with_condition

       
    # Crear un nuevo DataFrame con los resultados
    result_df = pd.DataFrame({
        "Original": values,
        "Modified": modified_values
    })
    
    return ranges, result_df

# Aplicar la función al vector del archivo
ranges, result_df = process_vector(data)


df_long = pd.concat([df_long, result_df.Modified], axis=1)


def clasificacion_strength(x):
    if  x == 0:
        return 'Neutro'
    elif x == 1:
        return 'Débil'
    elif x == 2:
        return 'Moderado'
    elif x == 3:
        return 'Fuerte'
    else:
        return 'Muy Fuerte'
    
df_long['type_class'] = df_long['Modified'].apply(clasificacion_strength)

df_long['type'] = df_long['type'].astype(int)

data.iloc[0:, 1].astype(int).tolist()

data = data['type'].astype(int)
