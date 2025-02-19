"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


import os
import re
import pandas as pd

def pregunta_01():
    # 1. Ruta al archivo 'clusters_report.txt'
    base_dir = os.path.dirname(__file__)
    txt_path = os.path.join(base_dir, "..", "files", "input", "clusters_report.txt")
    
    # 2. Leemos todas las líneas del archivo
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 3. Omitir las primeras 4 líneas (cabecera y separadores)
    data_lines = lines[4:]
    
    rows = []
    current_row = None
    
    # 4. Función para parsear la primera línea de cada cluster
    def parse_first_line(line):
        # Patrón para capturar:
        # 1) cluster (número entero)
        # 2) cantidad de palabras clave (entero)
        # 3) porcentaje de palabras clave (ej: "15,9")
        # 4) primeras palabras clave
        pattern = r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)$"
        match = re.match(pattern, line)
        if not match:
            return None
        
        cluster_str = match.group(1)
        cant_str = match.group(2)
        porc_str = match.group(3)
        palabras_str = match.group(4)
        
        # Convertir porcentaje de formato "15,9" a float 15.9
        porc_str = porc_str.replace(",", ".")
        porc_float = float(porc_str)
        
        return {
            "cluster": int(cluster_str),
            "cantidad_de_palabras_clave": int(cant_str),
            "porcentaje_de_palabras_clave": porc_float,
            "principales_palabras_clave": palabras_str.strip()
        }
    
    # 5. Procesar cada línea
    for line in data_lines:
        if not line.strip():
            continue
        
        first_line_data = parse_first_line(line)
        if first_line_data:
            if current_row is not None:
                rows.append(current_row)
            current_row = first_line_data
        else:
            # Si la línea es parte de las palabras clave, se concatena
            if current_row is not None:
                extra = line.strip()
                current_row["principales_palabras_clave"] += " " + extra
    
    # Agregar la última fila
    if current_row is not None:
        rows.append(current_row)
    
    # 6. Limpiar espacios múltiples en las palabras clave y quitar el punto final si existe
    for r in rows:
        texto = re.sub(r"\s+", " ", r["principales_palabras_clave"]).strip()
        # Eliminar el punto final si lo tiene
        if texto.endswith("."):
            texto = texto[:-1]
        r["principales_palabras_clave"] = texto
    
    # 7. Crear el DataFrame con el orden de columnas esperado
    df = pd.DataFrame(rows, columns=[
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave"
    ])
    
    return df


