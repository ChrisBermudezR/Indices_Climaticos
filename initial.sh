#!/usr/bin/env bash
# This script initializes the environment for the application.  

curl https://psl.noaa.gov/data/correlation/oni.data > ./data/oni.data
curl https://psl.noaa.gov/enso/mei/data/meiv2.data > ./data/meiv2.data
curl https://psl.noaa.gov/data/correlation/nina1.anom.data > ./data/nina1.anom.data
curl https://psl.noaa.gov/data/correlation/nina2.anom.data > ./data/nina2.anom.data
curl https://psl.noaa.gov/data/correlation/nina3.anom.data > ./data/nina3.anom.data
curl https://psl.noaa.gov/data/correlation/nina34.anom.data > ./data/nina3.4.anom.data
curl https://psl.noaa.gov/data/correlation/nina4.anom.data > ./data/nina4.anom.data
curl https://psl.noaa.gov/data/correlation/soi.data > ./data/soi.data