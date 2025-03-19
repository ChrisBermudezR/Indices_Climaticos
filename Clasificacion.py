# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 09:38:00 2024

@author: CBermudezr
"""

#Importar las librerías
import pandas as pd
import numpy as np

condicion = 5
anio_inicio = 1950
anio_fin = oni_entire_df_long['date'].iloc[-1].year
final_month = oni_entire_df_long['date'].iloc[-1].month
total_meses = pd.date_range(start=f'{anio_inicio}-01-01', end=f'{anio_fin}-{final_month}-01', freq='MS')
vector_index = np.array(oni_entire_df_long['value']).flatten()
vector_index = vector_index[:len(total_meses)]
    
    # Identificar periodos El Niño
pos_nino = np.where(vector_index >= 0.5)[0]
D = np.diff(np.concatenate(([0], np.diff(pos_nino) == 1, [0])))
pos_partida = np.where(D == 1)[0]
pos_llegada = np.where(D == -1)[0]
posiciones = np.vstack((pos_partida, pos_llegada))
resultado = np.diff(posiciones, axis=0)
posiciones_nino = np.where(resultado + 1 >= condicion)[1]
meses_nino = []

for i in posiciones_nino:
        periodos = pos_nino[pos_partida[i]:pos_llegada[i]]
        meses_nino.extend(total_meses[periodos])
        
Nino = pd.to_datetime(meses_nino)
    
Nino_event = pd.DataFrame({'date': Nino, 'event': 'Niño'})



    # Identificar periodos El Niña
    
pos_nina = np.where(vector_index <= -0.5)[0]
D = np.diff(np.concatenate(([0], np.diff(pos_nina) == 1, [0])))
pos_partida = np.where(D == 1)[0]
pos_llegada = np.where(D == -1)[0]
posiciones = np.vstack((pos_partida, pos_llegada))
resultado = np.diff(posiciones, axis=0)
posiciones_nina = np.where(resultado + 1 >= condicion)[1]
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
    

events_total=pd.concat([Nino_event, Nina_event, Neutro_event], axis=0)
events_total = events_total.sort_values(by='date')

 