"""
indexes.py
=================

Descripción:
------------
Este módulo procesa los datos de índices climáticos en formato wide que se
toman desde la NOAA y los transforma en formato long, para luego generar los
atributos necesarios para generar la 
los índices climáticos. 

Parámetros de entrada:
----------------------
- Un archivo `.csv` con los datos del índice climático (ONI).

Parámetros de salida:
---------------------
- Un archivo `.csv` procesado con las siguientes columnas:
    - `date`: Fecha del registro.
    - `value`: Valor del índice ONI.
    - `index_name`: Nombre del índice.
    - `index_description`: Descripción del índice.
    - `unit`: Unidad del índice.
    - `phase`: Fase climática (Neutra, Fría, o Cálida).
    - `phase_description`: Descripción de la fase.
    - `event`: Evento climático (Niño, Niña, Neutro).
    - `event_description`: Descripción del evento.
    - `type`: Clasificación de intensidad del evento.

Librerías requeridas:
---------------------
- `pandas >= 1.2`
- `eventClassifier` (con las funciones `oniClassifier` y `columnEvaluation`).

Notas:
------
- Este script está diseñado exclusivamente para trabajar con los índices ONI.
- Las clasificaciones de eventos se basan en un umbral de +/-0.5 °C en las anomalías de TSM y una duración mínima de 5 meses consecutivos.

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
from modules.eventClassifier import Classifier, columnEvaluation, MEIClassifier, SOIClassifier, IMTClassifier


"""
    Procesa un DataFrame del índice ONI para incluir información transformada y clasificaciones de eventos.

    Args:
        df (pd.DataFrame): DataFrame con las columnas:
            - `year`: Año del registro.
            - Meses como columnas con valores del índice ONI.

    Returns:
        pd.DataFrame: DataFrame transformado con las siguientes columnas:
            - `date`: Fecha (YYYY-MM-DD).
            - `value`: Valor del índice ONI.
            - `index_name`: Nombre del índice.
            - `index_description`: Descripción detallada del índice ONI.
            - `unit`: Unidad de medida (°C).
            - `phase`: Clasificación de fase climática ('Cálida', 'Fría', 'Neutra').
            - `phase_description`: Descripción de la fase climática.
            - `event`: Clasificación del evento climático ('Niño', 'Niña', 'Neutro').
            - `event_description`: Descripción del evento climático.
            - `type`: Clasificación de intensidad del evento.
"""


"""
ÍNDICE ONI

Oceanic Niño Index: From NOAA Climate Prediction Center (CPC)
Three month running mean of NOAA ERSST.V5 SST anomalies in the Niño 3.4 region 
(5N-5S, 120-170W), based on changing base period which onsist of multiple 
centered 30-year base periods. These 30-year base periods will be used to 
calculate the anomalies for successive 5-year periods in the historical record. 

"""

def oniIndex(df):
    # Transformar el DataFrame
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
    df_long['index_description'] = 'Índice Oceánico El Niño : Media móvil de 3 meses de las anomalías de la TSM ERSST.v5 en la región Niño 3.4 (5°N-5°S, 120°-170°W) Calculada a partir del ERSST V5 (en NOAA/CPC).'
    df_long['unit'] = '°C'

    # Crear una nueva columna 'Phase' con condiciones basadas en los valores de 'value'
    df_long['phase'] = df_long['value'].apply(lambda x: 'Fría' if x <= -0.5 else ('Cálida' if x >= 0.5 else 'Neutra'))
    df_long['phase_description'] = df_long['phase'].apply(lambda x: 'Esta fase se caracteriza porque las anomalías de TSM en la región 3.4 son inferiores a -0.5 °C' 
                                                    if x == 'Fría' else ('Esta fase se caracteriza porque las anomalías de TSM en la región 3.4 son superiores a 0.5 °C' 
                                                                      if x == 'Cálida'  else 'Esta fase se caracteriza porque las anomalías de TSM son inferiores a 0.5 °C y superiores a -0.5 °C'))

    # Identificar eventos
    event_total = Classifier(df_long, 5, -0.5, 0.5) # entradas de la función para el evenClassifier

    # Unir los eventos con el DataFrame original
    df_long = pd.merge(df_long, event_total, on='date')

    df_long['event_description'] = df_long['event'].apply(lambda x: 'Este evento se caracteriza porque la fase fría persiste durante al menos 5 meses consecutivos' 
                                                    if x == 'Niña' else ('Este evento se caracteriza porque la fase cálida persiste durante al menos 5 meses consecutivos' 
                                                                         if x == 'Niño' else 'Condiciones neutras'))
    
    df_long = columnEvaluation(df_long, 'event', 'value', 'type')
   

    return df_long

"""
ÍNDICE mei

Oceanic Niño Index: From NOAA Climate Prediction Center (CPC)
The bi-monthly Multivariate El Niño/Southern Oscillation (ENSO) index (MEI.v2) 
is the time series of the leading combined Empirical Orthogonal Function (EOF) 
of five different variables (sea level pressure (SLP), sea surface temperature (SST), 
zonal and meridional components of the surface wind, and outgoing longwave radiation (OLR)) 
over the tropical Pacific basin (30°S-30°N and 100°E-70°W).

"""

def meiIndex(df):
    # Transformar el DataFrame
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

    df_long['index_name'] = 'MEI'
    df_long['index_description'] = 'Índice Multivariado ENOS: v.2 El índice bimensual Multivariado de El Niño/Oscilación del Sur (ENSO) (MEI.v2) es la serie temporal de la principal Función Ortogonal Empírica (EOF, por sus siglas en inglés) combinada de seis variables diferentes: temperatura superficiel, temperatura del aire, presión atmosférica al nivel del mar, nubosidad, componente zonal del viento y componente meridional del viento en la cuenca del Pacífico tropical (30°S-30°N y 100°E-70°W) (en NOAA/CPC https://www.psl.noaa.gov/enso/mei/).'
    df_long['unit'] = 'dmless'

    # Crear una nueva columna 'Phase' con condiciones basadas en los valores de 'value'
    df_long['phase'] = df_long['value'].apply(lambda x: 'Fría' if x <= -0.5 else ('Cálida' if x >= 0.5 else 'Neutra'))
    
    df_long['phase_description'] = df_long['phase'].apply(lambda x: 'Esta fase se caracteriza por condiciones oceánicas y atmosféricas cálidas asociadas a El Niño (anomalías positivas del MEI)' 
                                                    if x == 'Cálida' else ('Esta fase se caracteriza por condiciones frías asociadas a La Niña (anomalías negativas del MEI)' 
                                                                        if x == 'Fría' else 'Esta fase se caracteriza por condiciones neutrales, sin predominancia de El Niño ni La Niña'))
    # Identificar eventos
    df_long = MEIClassifier (df_long) # entradas de la función para el evenClassifier

    

    df_long['event_description'] = df_long['event'].apply(lambda x: 'Este evento se caracteriza porque el valor del índice para el mes es igual o inferior al umbral de -0.5' 
                                                    if x == 'Niña' else ('Este evento se caracteriza porque el valor del índice para el mes es igual o supera el umbral de 0.5' 
                                                                         if x == 'Niño' else 'Este evento se caracteriza porque el valor del índice para el mes no supera el umbral de 0.5 y no es inferior al umbral de -0.5'))
    
    df_long['type'] = 'No aplicable'
   

    return df_long

"""
ÍNDICE NIÑO 1+2

Niño 1+2 Index: From NOAA Climate Prediction Center (CPC)
Extreme Eastern Tropical Pacific SST (0-10S, 90W-80W)
CPC uses the NOAA ERSST V5 anomalies. 
Now uses https://www.cpc.ncep.noaa.gov/data/indices/ersst5.nino.mth.91-20.ascii. 
Mean values also available.  

"""

def nino12Index(df):
    # Transformar el DataFrame
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

    df_long['index_name'] = 'Niño 1+2'
    df_long['index_description'] = 'Índice Niño 1+2: representa las anomalías mensuales de la temperatura superficial del mar (TSM) en la región más oriental del Pacífico ecuatorial, delimitada entre los 0°–10°S y 80°W–90°W, frente a las costas de Perú y Ecuador. Calculada a partir del ERSST V5 (en NOAA/CPC).'
    df_long['unit'] = '°C'

    # Crear una nueva columna 'Phase' con condiciones basadas en los valores de 'value'
    df_long['phase'] = df_long['value'].apply(lambda x: 'Fría' if x <= -0.5 else ('Cálida' if x >= 0.5 else 'Neutra'))
    df_long['phase_description'] = df_long['phase'].apply(lambda x: 'Esta fase se caracteriza porque las anomalías de TSM en la región 1+2 son inferiores a -0.5 °C' 
                                                    if x == 'Fría' else ('Esta fase se caracteriza porque las anomalías de TSM en la región 1+2 son superiores a 0.5 °C' 
                                                                      if x == 'Cálida'  else 'Esta fase se caracteriza porque las anomalías de TSM son inferiores a 0.5 °C y superiores a -0.5 °C'))

    # Identificar eventos
    event_total = Classifier(df_long, 5, -0.5, 0.5) # entradas de la función para el evenClassifier

    # Unir los eventos con el DataFrame original
    df_long = pd.merge(df_long, event_total, on='date')

    df_long['event_description'] = df_long['event'].apply(lambda x: 'Este evento se caracteriza porque la fase fría persiste durante al menos 5 meses consecutivos' 
                                                    if x == 'Niña' else ('Este evento se caracteriza porque la fase cálida persiste durante al menos 5 meses consecutivos' 
                                                                         if x == 'Niño' else 'Condiciones neutras'))
    
    df_long = columnEvaluation(df_long, 'event', 'value', 'type')
   

    return df_long


"""
ÍNDICE NIÑO 3

Niño 3 Index: From NOAA Climate Prediction Center (CPC)
Eastern Tropical Pacific SST (5N-5S,150W-90W): From NOAA Climate Prediction Center(CPC)
CPC uses the NOAA ERSST V5 anomalies. Now uses https://www.cpc.ncep.noaa.gov/data/indices/ersst5.nino.mth.91-20.ascii. Mean values also available.   

"""

def nino3Index(df):
    # Transformar el DataFrame
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

    df_long['index_name'] = 'Niño 3'
    df_long['index_description'] = 'Índice Niño 3: El índice Niño 3 corresponde a las anomalías mensuales de la temperatura superficial del mar (TSM) en la región del Pacífico ecuatorial comprendida entre los 5°N–5°S y 90°W–150°W. Calculada a partir del ERSST V5 (en NOAA/CPC).'
    df_long['unit'] = '°C'

    # Crear una nueva columna 'Phase' con condiciones basadas en los valores de 'value'
    df_long['phase'] = df_long['value'].apply(lambda x: 'Fría' if x <= -0.5 else ('Cálida' if x >= 0.5 else 'Neutra'))
    df_long['phase_description'] = df_long['phase'].apply(lambda x: 'Esta fase se caracteriza porque las anomalías de TSM en la región 3 son inferiores a -0.5 °C' 
                                                    if x == 'Fría' else ('Esta fase se caracteriza porque las anomalías de TSM en la región 3 son superiores a 0.5 °C' 
                                                                      if x == 'Cálida'  else 'Esta fase se caracteriza porque las anomalías de TSM son inferiores a 0.5 °C y superiores a -0.5 °C'))

    # Identificar eventos
    event_total = Classifier(df_long, 5, -0.5, 0.5) # entradas de la función para el evenClassifier

    # Unir los eventos con el DataFrame original
    df_long = pd.merge(df_long, event_total, on='date')

    df_long['event_description'] = df_long['event'].apply(lambda x: 'Este evento se caracteriza porque la fase fría persiste durante al menos 5 meses consecutivos' 
                                                    if x == 'Niña' else ('Este evento se caracteriza porque la fase cálida persiste durante al menos 5 meses consecutivos' 
                                                                         if x == 'Niño' else 'Condiciones neutras'))
    
    df_long = columnEvaluation(df_long, 'event', 'value', 'type')
   

    return df_long


"""
ÍNDICE NIÑO 3.4

Niño 3 Index: From NOAA Climate Prediction Center (CPC)
East Central Tropical Pacific SST (5N-5S)(170-120W): From CPC
CPC uses the NOAA ERSST V5 anomalies. Now uses https://www.cpc.ncep.noaa.gov/data/indices/ersst5.nino.mth.91-20.ascii. Mean values also available. 
"""

def nino34Index(df):
    # Transformar el DataFrame
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

    df_long['index_name'] = 'Niño 3.4'
    df_long['index_description'] = 'Índice Niño 3.4: El índice Niño 3.4 mide las anomalías mensuales de la temperatura superficial del mar (TSM) en la región comprendida entre los 5°N–5°S y 120°W–170°W del Pacífico central ecuatorial. Calculada a partir del ERSST V5 (en NOAA/CPC).'
    df_long['unit'] = '°C'

    # Crear una nueva columna 'Phase' con condiciones basadas en los valores de 'value'
    df_long['phase'] = df_long['value'].apply(lambda x: 'Fría' if x <= -0.5 else ('Cálida' if x >= 0.5 else 'Neutra'))
    df_long['phase_description'] = df_long['phase'].apply(lambda x: 'Esta fase se caracteriza porque las anomalías de TSM en la región 3.4 son inferiores a -0.5 °C' 
                                                    if x == 'Fría' else ('Esta fase se caracteriza porque las anomalías de TSM en la región 3.4 son superiores a 0.5 °C' 
                                                                      if x == 'Cálida'  else 'Esta fase se caracteriza porque las anomalías de TSM son inferiores a 0.5 °C y superiores a -0.5 °C'))

    # Identificar eventos
    event_total = Classifier(df_long, 5, -0.5, 0.5) # entradas de la función para el evenClassifier

    # Unir los eventos con el DataFrame original
    df_long = pd.merge(df_long, event_total, on='date')

    df_long['event_description'] = df_long['event'].apply(lambda x: 'Este evento se caracteriza porque la fase fría persiste durante al menos 5 meses consecutivos' 
                                                    if x == 'Niña' else ('Este evento se caracteriza porque la fase cálida persiste durante al menos 5 meses consecutivos' 
                                                                         if x == 'Niño' else 'Condiciones neutras'))
    
    df_long = columnEvaluation(df_long, 'event', 'value', 'type')
   

    return df_long

"""
ÍNDICE NIÑO 4

Central Tropical Pacific SST (5N-5S) (160E-150W): From CPC
CPC uses the NOAA ERSST V5 anomalies. Now uses https://www.cpc.ncep.noaa.gov/data/indices/ersst5.nino.mth.91-20.ascii. Mean values also available. 

"""

def nino4Index(df):
    # Transformar el DataFrame
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

    df_long['index_name'] = 'Niño 4'
    df_long['index_description'] = 'Índice Niño 4: El índice Niño 4 representa las anomalías mensuales de la temperatura superficial del mar (TSM) en la región del Pacífico ecuatorial occidental, delimitada entre los 5°N–5°S y 160°E–150°W. Calculada a partir del ERSST V5 (en NOAA/CPC).'
    df_long['unit'] = '°C'

    # Crear una nueva columna 'Phase' con condiciones basadas en los valores de 'value'
    df_long['phase'] = df_long['value'].apply(lambda x: 'Fría' if x <= -0.5 else ('Cálida' if x >= 0.5 else 'Neutra'))
    df_long['phase_description'] = df_long['phase'].apply(lambda x: 'Esta fase se caracteriza porque las anomalías de TSM en la región 4 son inferiores a -0.5 °C' 
                                                    if x == 'Fría' else ('Esta fase se caracteriza porque las anomalías de TSM en la región 4 son superiores a 0.5 °C' 
                                                                      if x == 'Cálida'  else 'Esta fase se caracteriza porque las anomalías de TSM son inferiores a 0.5 °C y superiores a -0.5 °C'))

    # Identificar eventos
    event_total = Classifier(df_long, 5, -0.5, 0.5) # entradas de la función para el evenClassifier

    # Unir los eventos con el DataFrame original
    df_long = pd.merge(df_long, event_total, on='date')

    df_long['event_description'] = df_long['event'].apply(lambda x: 'Este evento se caracteriza porque la fase fría persiste durante al menos 5 meses consecutivos' 
                                                    if x == 'Niña' else ('Este evento se caracteriza porque la fase cálida persiste durante al menos 5 meses consecutivos' 
                                                                         if x == 'Niño' else 'Condiciones neutras'))
    
    df_long = columnEvaluation(df_long, 'event', 'value', 'type')
   

    return df_long


"""
ÍNDICE SOI

"""

def soiIndex(df):
    # Transformar el DataFrame
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
    
    df_long['index_name'] = 'SOI'
    df_long['index_description'] = 'Southern Oscillation Index: El Índice de la Oscilación del Sur es un indicador climático que mide la diferencia de presión atmosférica a nivel del mar entre dos estaciones del Pacífico tropical: Tahití (Polinesia Francesa) y Darwin (Australia). Calculada a partir del ERSST V5 (en NOAA/CPC https://www.psl.noaa.gov/data/timeseries/month/DS/SOI/).'
    df_long['unit'] = 'dmLess'

    # Crear una nueva columna 'Phase' con condiciones basadas en los valores de 'value'
    df_long['phase'] = df_long['value'].apply(lambda x: 'Fría' if x > 0 else ('Cálida' if x < 0 else 'Neutra'))
    df_long['phase_description'] = df_long['phase'].apply(lambda x: 'Esta fase se caracteriza por presiones más bajas en Tahití y más altas en Darwin, típicas de El Niño (SOI negativo)' 
                                                    if x == 'Cálida' else ('Esta fase se caracteriza por presiones más altas en Tahití y más bajas en Darwin, típicas de La Niña (SOI positivo)'       
                                                                           if x == 'Fría' else 'Esta fase se caracteriza por condiciones neutrales, sin predominancia de El Niño ni La Niña'))
    # Identificar eventos
    event_total = SOIClassifier (df_long, 5, -0.7, 0.7) # entradas de la función para el evenClassifier

    # Unir los eventos con el DataFrame original
    df_long = pd.merge(df_long, event_total, on='date')

    df_long['event_description'] = df_long['event'].apply(lambda x: 'Este evento se caracteriza porque el valor del índice para el mes es positivo' 
                                                    if x == 'Niña' else ('Este evento se caracteriza porque el valor del índice para el mes es negativo' 
                                                                         if x == 'Niño' else 'Este evento se caracteriza porque el valor del índice para el mes es cero'))
    
    df_long['type'] = 'No aplicable'
   

    return df_long

"""
ÍNDICE IMT

"""

def IMTIndex(df):
    # Transformar el DataFrame
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
    
    df_long['index_name'] = 'IMT'
    df_long['index_description'] = 'El Índice Multivariado de Tumaco (IMT) es un indicador climático utilizado para monitorear las condiciones oceánicas y atmosféricas en la región del Pacífico colombiano, específicamente en la ensenada de Tumaco. Este índice integra múltiples variables meteorológicas y oceanográficas para evaluar fenómenos como El Niño y La Niña, así como condiciones neutras en la zona. (en DIMAR/CCCP https://cccp.dimar.mil.co/IMT).'
    df_long['unit'] = 'dmLess'

    # Crear una nueva columna 'Phase' con condiciones basadas en los valores de 'value'
    df_long['phase'] = IMTClassifier(df_long['value'])
    
    
    fase_descripcion = {
        'C5': 'Fase cálida muy fuerte',
        'C4': 'Fase cálida muy fuerte',
        'C3': 'Fase cálida fuerte',
        'C2': 'Fase cálida moderada',
        'C1': 'Fase cálida neutra',
        'F1': 'Fase fría neutra',
        'F2': 'Fase fría moderada',
        'F3': 'Fase fría fuerte',
        'F4': 'Fase fría muy fuerte',
        'F5': 'Fase fría muy fuerte'
    }

    
    df_long['phase_description'] = df_long['phase'].apply(lambda x: fase_descripcion.get(x, 'Fase desconocida'))


    # Identificar eventos
    event_total = SOIClassifier (df_long, 5, -0.7, 0.7) # entradas de la función para el evenClassifier

    # Unir los eventos con el DataFrame original
    df_long = pd.merge(df_long, event_total, on='date')

    df_long['event_description'] = df_long['event'].apply(lambda x: 'Este evento se caracteriza porque el valor del índice para el mes es positivo' 
                                                    if x == 'Niña' else ('Este evento se caracteriza porque el valor del índice para el mes es negativo' 
                                                                         if x == 'Niño' else 'Este evento se caracteriza porque el valor del índice para el mes es cero'))
    
    df_long['type'] = 'No aplicable'
   

    return df_long


"""
ÍNDICE RONI

Warm (red) and cold (blue) periods based on a threshold of +/- 0.5°C for the Relative Oceanic Niño Index (RONI), 
using the 1991–2020 base period [3 month running mean of ERSST.v5 SST anomalies in the Niño 3.4 region (5°N–5°S, 120°–170°W) 
with average tropical mean (20°N–20°S) SST anomalies subtracted. The difference is then adjusted so the variance equals the 
original Niño 3.4 index].

For historical purposes, periods of below and above normal SSTs are colored in blue and red when the threshold is met 
for a minimum of five (5) consecutive overlapping seasons. The RONI is one measure of the El Niño Southern Oscillation, 
and other indices can confirm whether features consistent with a coupled ocean-atmosphere phenomenon accompanied these periods.

"""

def roniIndex(df):
    # Transformar el DataFrame
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

    df_long['index_name'] = 'RONI'
    df_long['index_description'] = 'Índice Oceánico Relativo El Niño  : Media móvil de 3 meses de las anomalías de la TSM ERSST.v5 calculadas usando el período base 1991–2020 [promedio móvil de 3 meses de las anomalías de la temperatura superficial del mar (SST) ERSST.v5 en la región Niño 3.4 (5°N - 5°S, 120° - 170°O), con las anomalías promedio de SST de los trópicos (20°N - 20°S) restadas. Luego, la diferencia se ajusta para que la varianza sea igual a la del índice original de Niño 3.4] (en NOAA/CPC).'
    df_long['unit'] = '°C'

    # Crear una nueva columna 'Phase' con condiciones basadas en los valores de 'value'
    df_long['phase'] = df_long['value'].apply(lambda x: 'Fría' if x <= -0.5 else ('Cálida' if x >= 0.5 else 'Neutra'))
    df_long['phase_description'] = df_long['phase'].apply(lambda x: 'Esta fase se caracteriza porque las anomalías de TSM en la región 3.4 son inferiores a -0.5 °C' 
                                                    if x == 'Fría' else ('Esta fase se caracteriza porque las anomalías de TSM en la región 3.4 son superiores a 0.5 °C' 
                                                                      if x == 'Cálida'  else 'Esta fase se caracteriza porque las anomalías de TSM son inferiores a 0.5 °C y superiores a -0.5 °C'))

    # Identificar eventos
    event_total = Classifier(df_long, 5, -0.5, 0.5) # entradas de la función para el evenClassifier

    # Unir los eventos con el DataFrame original
    df_long = pd.merge(df_long, event_total, on='date')

    df_long['event_description'] = df_long['event'].apply(lambda x: 'Este evento se caracteriza porque la fase fría persiste durante al menos 5 meses consecutivos' 
                                                    if x == 'Niña' else ('Este evento se caracteriza porque la fase cálida persiste durante al menos 5 meses consecutivos' 
                                                                         if x == 'Niño' else 'Condiciones neutras'))
    
    df_long = columnEvaluation(df_long, 'event', 'value', 'type')
   

    return df_long


