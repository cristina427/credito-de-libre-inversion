import os
import json


def obtener_json_reciente():

    archivos = os.listdir("entrada")

    archivo = archivos[0]

    print(f"Archivo encontrado: {archivo}")
    ruta = os.path.join("entrada", archivo)

    with open(ruta, "r", encoding="utf-8") as archivo_json:
     datos = json.load(archivo_json)

    print(datos)
    novedades = datos["novedades"]

    print(novedades)

    print(f"Total novedades: {len(novedades)}")
