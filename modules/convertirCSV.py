
import os
import re
import pandas as pd

def dataprocesser(folder_path, expected_months=12):
    
    folder_raw = os.path.join(folder_path,"raw")
    
    for file_name in os.listdir(folder_raw):
        file_path = os.path.join(folder_raw, file_name)
        file_outpath = os.path.join(folder_path, "processed")
        
        if not os.path.isfile(file_path):
            continue

        print(f"Procesando archivo: {file_name}")

        with open(file_path, 'r') as file:
            lines = file.readlines()

        data = []
        bad_rows = 0

        for line in lines:
            line = line.strip()
            if not line or line.startswith("Nino") or "https://" in line:
                continue

            columns = re.split(r"\s+", line)
            if len(columns) < 2:
                bad_rows += 1
                continue

            try:
                year = int(columns[0])
            except ValueError:
                bad_rows += 1
                continue

            raw_values = columns[1:]

            # Normaliza a EXACTAMENTE expected_months
            normalized = []
            for i in range(expected_months):
                if i < len(raw_values):
                    v = raw_values[i]
                    if v in {'-99.90','-99.99', '-999',  '-99', 'NA', 'NaN', 'nan', '-999.0'}:
                        normalized.append(None)
                    else:
                        try:
                            normalized.append(float(v))
                        except ValueError:
                            normalized.append(None)
                else:
                    normalized.append(None)

            data.append([year] + normalized)

        if not data:
            print(f"No se encontraron datos válidos en {file_name}")
            continue

        column_names = ['year'] + [f"{m:02d}" for m in range(1, expected_months + 1)]
        df = pd.DataFrame(data, columns=column_names)

        output_file = os.path.join(file_outpath, f"{os.path.splitext(file_name)[0]}.csv")
        df.to_csv(output_file, sep=',', header=True, index=False)
        print(f"Archivo guardado: {output_file} (líneas descartadas/atípicas: {bad_rows})")
