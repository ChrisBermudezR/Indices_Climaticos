"""
eventClassifier.py
=================

Este módulo contiene funciones necesarias para clasificar índices climáticos como ONI 
y evaluar otros atributos requeridos para el seguimiento de El Niño Oscilación Sur.

Descripción:
------------
- `oniClassifier`: Identifica eventos climáticos (El Niño, La Niña y Neutro) basados en un índice climático (ONI).
- `typeClassifier`: Clasifica un valor numérico en categorías según su intensidad.
- `columnEvaluation`: Evalúa y clasifica valores de dos columnas en un DataFrame, creando una nueva columna con la clasificación.

Parámetros de entrada:
----------------------
- `oniClassifier`: 
    - `data` (pd.DataFrame): DataFrame con las fechas y valores del índice climático.
    - `condicion` (int): Número mínimo de meses consecutivos para definir un evento.
    - `umbral_inferior` (float): Umbral inferior para clasificar eventos La Niña.
    - `umbral_superior` (float): Umbral superior para clasificar eventos El Niño.
- `typeClassifier`:
    - `x` (float): Valor numérico a clasificar.
- `columnEvaluation`:
    - `df` (pd.DataFrame): DataFrame a evaluar.
    - `col1` (str): Nombre de la primera columna.
    - `col2` (str): Nombre de la segunda columna.
    - `nueva_col` (str): Nombre de la columna resultante.

Parámetros de salida:
---------------------
- `oniClassifier`: DataFrame con eventos clasificados (El Niño, La Niña, Neutro).
- `typeClassifier`: Categoría de intensidad como cadena de texto.
- `columnEvaluation`: DataFrame con una nueva columna basada en las condiciones.

Librerías requeridas:
---------------------
- `pandas >=  1.5.3`
- `numpy >= 1.24.3`

Notas:
------
- Este script está diseñado específicamente para índices climáticos ONI y eventos relacionados.
- Asegúrate de que los datos de entrada tengan un formato adecuado antes de usar las funciones.

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
import numpy as np

def Classifier(data, condicion, umbral_inferior, umbral_superior):
    
    """
    Clasifica eventos climáticos (El Niño, La Niña y Neutro) basados en el índice ONI.

    Args:
        data (pd.DataFrame): DataFrame con las columnas 'date' (fechas) y 'value' (índices ONI).
        condicion (int): Número mínimo de meses consecutivos para definir un evento.
        umbral_inferior (float): Umbral inferior para La Niña.
        umbral_superior (float): Umbral superior para El Niño.

    Returns:
        pd.DataFrame: DataFrame con eventos clasificados por fecha y tipo ('Niño', 'Niña', 'Neutro').
    """
   
    anio_inicio = 1950
    anio_fin = data['date'].iloc[-1].year
    final_month = data['date'].iloc[-1].month
    total_meses = pd.date_range(start=f'{anio_inicio}-01-01', end=f'{anio_fin}-{final_month}-01', freq='MS')
    vector_index = np.array(data['value']).flatten()
    vector_index = vector_index[:len(total_meses)]
    
    # Identificar periodos El Niño
    pos_nino = np.where(vector_index >= umbral_superior)[0]
    D = np.diff(np.concatenate(([0], np.diff(pos_nino) == 1, [0])))
    pos_partida = np.where(D == 1)[0]
    pos_llegada = np.where(D == -1)[0]+1
    posiciones = np.vstack((pos_partida, pos_llegada))
    resultado = np.diff(posiciones, axis=0)
    posiciones_nino = np.where(resultado >= condicion)[1]
    meses_nino = []

    for i in posiciones_nino:
        periodos = pos_nino[pos_partida[i]:pos_llegada[i]]
        meses_nino.extend(total_meses[periodos])
        
    Nino = pd.to_datetime(meses_nino)
    Nino_event = pd.DataFrame({'date': Nino, 'event': 'Niño'})

    # Identificar periodos La Niña
    pos_nina = np.where(vector_index <= umbral_inferior)[0]
    D = np.diff(np.concatenate(([0], np.diff(pos_nina) == 1, [0])))
    pos_partida = np.where(D == 1)[0]
    pos_llegada = np.where(D == -1)[0]+1
    posiciones = np.vstack((pos_partida, pos_llegada))
    resultado = np.diff(posiciones, axis=0)
    posiciones_nina = np.where(resultado >= condicion)[1]
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

    return pd.concat([Nino_event, Nina_event, Neutro_event]).sort_values(by='date').reset_index(drop=True)

def typeClassifier(x):
    
    """
    Clasifica un valor numérico en una categoría basada en rangos.

    Args:
        x (float): El valor numérico a clasificar.

    Returns:
        str: La categoría en la que cae el valor.
    """
    if -0.5 < x < 0.5:
        return 'Neutro'
    elif 0.5 <= x < 1.0 or -1.0 < x <= -0.5:
        return 'Débil'
    elif 1.0 <= x < 1.5 or -1.5 < x <= -1.0:
        return 'Moderado'
    elif 1.5 <= x < 2.0 or -2.0 < x <= -1.5:
        return 'Fuerte'
    else:
        return 'Muy Fuerte'
    
def columnEvaluation(df, col1, col2, nueva_col):

    """
  Evalúa dos columnas en un DataFrame y crea una nueva columna basada en las condiciones especificadas.

  Args:
      df (pd.DataFrame): DataFrame con las columnas a evaluar.
      col1 (str): Nombre de la primera columna a evaluar.
      col2 (str): Nombre de la segunda columna a clasificar.
      nueva_col (str): Nombre de la columna resultante.

  Returns:
      pd.DataFrame: DataFrame con la nueva columna añadida.
  """

    def conditions(row):

        if 'Neutro' in row[col1]:

            return 'Neutro'

        else:

            return typeClassifier(row[col2])


    df[nueva_col] = df.apply(conditions, axis=1)

    return df

def meiClassifier(data, condicion, umbral_inferior, umbral_superior):
        
        """
        Clasifica eventos climáticos (El Niño, La Niña y Neutro) basados en el índice MEI.
    
        Args:
            data (pd.DataFrame): DataFrame con las columnas 'date' (fechas) y 'value' (índices MEI).
            condicion (int): Número mínimo de meses consecutivos para definir un evento.
            umbral_inferior (float): Umbral inferior para La Niña.
            umbral_superior (float): Umbral superior para El Niño.
    
        Returns:
            pd.DataFrame: DataFrame con eventos clasificados por fecha y tipo ('Niño', 'Niña', 'Neutro').
        """
    
        anio_inicio = 1950
        anio_fin = data['date'].iloc[-1].year
        final_month = data['date'].iloc[-1].month
        total_meses = pd.date_range(start=f'{anio_inicio}-01-01', end=f'{anio_fin}-{final_month}-01', freq='MS')
        vector_index = np.array(data['value']).flatten()
        vector_index = vector_index[:len(total_meses)]
        
        # Identificar periodos El Niño
        pos_nino = np.where(vector_index >= umbral_superior)[0]
        D = np.diff(np.concatenate(([0], np.diff(pos_nino) == 1, [0])))
        pos_partida = np.where(D == 1)[0]
        pos_llegada = np.where(D == -1)[0]+1
        posiciones = np.vstack((pos_partida, pos_llegada))
        resultado = np.diff(posiciones, axis=0)
        posiciones_nino = np.where(resultado >= condicion)[1]
        meses_nino = []
    
        for i in posiciones_nino:
            periodos = pos_nino[pos_partida[i]:pos_llegada[i]]
            meses_nino.extend(total_meses[periodos])
            
        Nino = pd.to_datetime(meses_nino)
        Nino_event = pd.DataFrame({'date': Nino, 'event': 'Niño'})
    
        # Identificar periodos La Niña
        pos_nina = np.where(vector_index <= umbral_inferior)[0]
        D = np.diff(np.concatenate(([0], np.diff(pos_nina) == 1, [0])))
        pos_partida = np.where(D == 1)[0]  
