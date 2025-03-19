function [Nino,Nina,Neutro,meses_Procesados] = condiciones_ENOS(indice,t,umbral_nina,umbral_nino)
    %% Periodo de análisis
    condicion = 3;
    anio_inicio = 1950;
    anio_fin = year(t(end));    
    total_meses = datetime(anio_inicio,1,15):calmonths:datetime(anio_fin,month(t(end)),15);
    vector_index = indice(:); % Convertir matriz en vector para simplificar la identificación.
    vector_index = vector_index(1:length(total_meses)); % Limitar vector a periodo de interés.
    
    
    %% Identificar periodos El Niño
    pos_nino = find(vector_index >= umbral_nino); % Identificar posiciones de anomalías >= al umbral.
    D = diff([0,diff(pos_nino)==1,0]); 
    
    % Identificar posiciones cuya resta es igual a 1.
    pos_partida = find(D == 1); % Almacenar la posición de los puntos de partida.
    pos_llegada = find(D == -1); % Almacenar la posición de los puntos de llegada.
    posiciones = [pos_partida; pos_llegada]; % Construir matriz: Fila 1, posiciones de partida; fila 2, posiciones de llegada. 
    resultado = diff(posiciones); % Resta matricial: Posiciones de llegada - Posiciones de partida. Cantidad de meses por encima del umbral. 
    posiciones_nino = find(resultado + 1 >= condicion); % Identfica posiciones que satisfacen el criterio de al menos 5 meses consecutivos por sobre (o debajo) del umbral.  
    cont = 0; % Variable de control para actualizar índice.
    for i = 1 : length(posiciones_nino)
    periodos = pos_nino(pos_partida(posiciones_nino(i)):pos_llegada(posiciones_nino(i))); % Extraer y almacenar posiciones de periodos que superaron el umbral por al menos 5 meses.
    meses_nino(cont + 1 : cont + length(total_meses(periodos))) = total_meses(periodos); % Almacenar meses que cumplieron el criterio.
    cont = length(meses_nino); % Actualizar índice.
    end
    Nino = meses_nino; % Retornar periodos El Niño.
    
    
    
    %% Identificar periodos La Niña.
    pos_nina = find(vector_index <= umbral_nina); % Identificar posiciones de anomalías <= al umbral.
    D = diff([0,diff(pos_nina')==1,0]); % Identificar posiciones cuya resta es igual a 1.
    pos_partida = find(D == 1); % Almacenar la posición de los puntos de partida.
    pos_llegada = find(D == -1); % Almacenar la posición de los puntos de llegada.
    posiciones = [pos_partida; pos_llegada]; % Construir matriz: Fila 1, posiciones de partida; fila 2, posiciones de llegada. 
    resultado = diff(posiciones); % Resta matricial: Posiciones de llegada - Posiciones de partida. Cantidad de meses por encima del umbral. 
    posiciones_nina = find(resultado + 1 >= condicion); % Identfica posiciones que satisfacen el criterio de al menos 5 meses consecutivos por sobre (o debajo) del umbral.  
    cont = 0; % Variable de control para actualizar índice.
    for i = 1 : length(posiciones_nina)
    periodos = pos_nina(pos_partida(posiciones_nina(i)):pos_llegada(posiciones_nina(i))); % Extraer y almacenar posiciones de periodos que superaron el umbral por al menos 5 meses.
    meses_nina(cont + 1 : cont + length(total_meses(periodos))) = total_meses(periodos); % Almacenar meses que cumplieron el criterio.
    cont = length(meses_nina); % Actualizar índice.
    end
    Nina = meses_nina; % Retornar periodos La Niña.
    %% Identificar periodos Neutros.
    pos_neutro_1 = ismember(total_meses,Nino); % Posición de periodos Niño.
    pos_neutro_2 = ismember(total_meses,Nina); % Posición de periodos Niña.
    Neutro = total_meses(pos_neutro_1 ~= 1 & pos_neutro_2 ~= 1); % Meses de periodos neutros.
    %% Meses procesados
    meses_Procesados = total_meses; % Retornar meses procesados.
end