#!/usr/bin/env bash
# This script initializes the environment for the application.  

# Create data directory if it doesn't exist
mkdir -p ./data

# Download necessary data files
echo 'Inicializando entorno...'
echo 'Descargando datos...'
curl https://psl.noaa.gov/data/correlation/oni.data > ./data/raw/oni.data
curl https://psl.noaa.gov/enso/mei/data/meiv2.data > ./data/raw/meiv2.data
curl https://psl.noaa.gov/data/correlation/nina1.anom.data > ./data/raw/nina1.data
curl https://psl.noaa.gov/data/correlation/nina3.anom.data > ./data/raw/nina3.data
curl https://psl.noaa.gov/data/correlation/nina34.anom.data > ./data/raw/nina34.data
curl https://psl.noaa.gov/data/correlation/nina4.anom.data > ./data/raw/nina4.data
curl https://psl.noaa.gov/data/correlation/soi.data > ./data/raw/soi.data
echo 'Datos descargados.'

# Process data with Python script
echo 'Procesando datos con python...'
python3 main.py
echo 'Datos procesados.'
