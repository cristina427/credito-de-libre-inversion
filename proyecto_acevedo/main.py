from modulos.configuracion import cargar_configuracion
from modulos.lectura import obtener_json_reciente

parametros = cargar_configuracion()

print(parametros)

obtener_json_reciente()
