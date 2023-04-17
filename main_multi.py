import os
from multi_infracciones_sutran import obtener_datos_papeletas
from multi_verificar_sutran import verificar_papeletas
from multi_cinemometro_foto import obtener_fotos
from query_vehiculos_graphql import query_vehiculos
from eliminar_repetidas import eliminar_repetidas
from subir_archivos import subir_archivos
from subir_graphql import subir_graphql
from listar_correos import listar_correos
from enviar_correos import enviar_correos
from dotenv import load_dotenv
from query_vehiculos_csv import query_vehiculos_csv
from unir_placas_clientes_supervisores_csv import unir_placas_clientes_supervisores_csv
import pandas as pd

load_dotenv()
NOMBRE_TABLA_VEHICULOS = os.getenv("NOMBRE_TABLA_VEHICULOS")
NOMBRE_TABLA_PAPELETAS = os.getenv("NOMBRE_TABLA_PAPELETAS")
NOMBRE_BUCKET_S3 = os.getenv("NOMBRE_BUCKET_S3")
PATH_PUBLIC = os.getenv("PATH_PUBLIC")
GRAPHQL_ENDPOINT = os.getenv("GRAPHQL_ENDPOINT")
API_KEY = os.getenv("API_KEY")
ruta_placas_cliente = "placas_cliente_detalles.csv"
ruta_cliente_supervisor = "cliente_supervisor.csv"


# Es una lista de placa, cliente y vehiculoID en JSON
def eliminar_guion(placa):
    placa_sin_guion = placa.replace("-", "")
    return placa_sin_guion


# lista_vehiculos_query = query_vehiculos(
#     NOMBRE_TABLA_VEHICULOS, GRAPHQL_ENDPOINT, API_KEY
# )
# df_placas_clientes_supervisores = query_vehiculos_csv()
df_placas_clientes_supervisores = pd.read_csv(
    "total_placa_cliente_supervisor_vanilla.csv", encoding="ISO-8859-1"
)
# print(lista_vehiculos_query)
# Tabla placas
# De la lista de placas, debo obtener el valor del cliente. Como un vlookup
# Del valor cliente, obtener el supervisor y su correo
# Part Key | Sort Key | Supervisor | Correo Supervisor
# PLACA | Cliente | Supervisor | Correo Supervisor


# Esta tabla la debería sacar de Cliente
# Cliente | Supervisor | Correo supervisor | Correo administrador
# Supervisor | Correo
# lista_correos_supervisores_query = ["diego_1021_@outlook.com", "diego.pizarro@pucp.pe"]


# lista_vehiculos_query = [
#     {"placa": "ATF761", "cliente": "LAS BAMBAS"},
#     {"placa": "ATF716", "cliente": "LAS BAMBAS"},
#     {"placa": "ATE939", "cliente": "LAS BAMBAS"},
#     {"placa": "ATF894", "cliente": "LAS BAMBAS"},
#     {"placa": "ATF893", "cliente": "LAS BAMBAS"},
#     {"placa": "ATF842", "cliente": "LAS BAMBAS"},
#     {"placa": "BKD764", "cliente": "SAN FERNANDO S.A"},
# ]

df_placas_cliente = pd.read_csv(ruta_placas_cliente, encoding="ISO-8859-1")
# df_cliente_supervisor = pd.read_csv(ruta_cliente_supervisor, encoding="ISO-8859-1")
# df_total = df_placas_cliente.merge(df_cliente_supervisor, how="left", on="cliente")

# Eliminar guiones
df_placas_cliente["placa"] = df_placas_cliente["placa"].apply(eliminar_guion)
cant_placas = len(df_placas_cliente.index)

lista_vehiculos_query = []

# print(len(df_total.index))
# for x in range(6):
# for x in range(cant_placas):
for x in range(628, 630):
    lista_vehiculos_query.append(
        {
            "placa": df_placas_cliente["placa"][x],
            "cliente": df_placas_cliente["cliente"][x],
        }
    )
lista_placa_query = []
lista_cliente_query = []
# lista_id_query = []

for v in lista_vehiculos_query:
    lista_placa_query.append(v["placa"])
    lista_cliente_query.append(v["cliente"])
    # lista_id_query.append(v["id"])


# lista_placas_query = ["BKD764", "BLV785", "BDN910", "BEB884", "BEB741", "BHM942", "ATE776", "ATE778", "ATE880", "ATE914", "ATE937" "ATE938", "ATE939", "ATE940", "ATF713", "ATF714",
#                       "ATF715", "ATF716", "ATF720", "ATF730", "ATF747", "ATF748", "ATF749", "ATF752", "ATF761", "ATF762", "ATF763", "ATF765",
#                       "ATF777", "ATF789", "ATF790", "ATF791", "ATF792", "ATF837", "ATF841", "ATF842", "ATF843", "ATF845",
#                       "ATF855", "ATF884", "ATO907", "ATO910", "ATO912", "ATO916", "ATR722", "ATR727", "AUD787", "AVE847"]

dict_datos = obtener_datos_papeletas(lista_placa_query)

dict_papeletas_nuevas = eliminar_repetidas(
    NOMBRE_TABLA_PAPELETAS, dict_datos, GRAPHQL_ENDPOINT, API_KEY
)

if len(dict_papeletas_nuevas["numdocumento"]) > 0:
    dict_verificar = verificar_papeletas(dict_papeletas_nuevas, lista_vehiculos_query)

    # Aquí deberían figurar los clientes

    del dict_verificar["numdocumento"]

    dict_verificar_nuevas = dict_papeletas_nuevas | dict_verificar

    dict_fotos = obtener_fotos(dict_verificar_nuevas, NOMBRE_BUCKET_S3, PATH_PUBLIC)
    del dict_fotos["numdocumento"]

    papeletas_dict = dict_verificar_nuevas | dict_fotos
    print("papeletas_dict")
    print(papeletas_dict)
    # Para los correos necesito:
    # Cliente, placas, fechas, monto, monto pronto pago, numdocumento, path /tmp/ (para adjuntar el archivo), correo supervisor, correo comercial
    c = listar_correos(papeletas_dict, ruta_cliente_supervisor)
    lista_para_enviar_correos = c[0]
    papeletas_con_correo = c[1]
    # print(lista)
    # enviar_correos(lista_para_enviar_correos)
    subir_graphql(
        NOMBRE_TABLA_PAPELETAS,
        papeletas_con_correo,
        lista_placa_query,
        GRAPHQL_ENDPOINT,
        API_KEY,
    )
    print(papeletas_dict)
    subir_archivos(NOMBRE_BUCKET_S3, PATH_PUBLIC, papeletas_dict)


else:
    print("No hay papeletas nuevas!")
