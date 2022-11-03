import requests
from bs4 import BeautifulSoup
import pandas as pd
import boto3
import time
import datetime
from datetime import timezone

client = boto3.client("dynamodb")

lista_write_sutran = []
lista_write_satlima = []
lista_write_callao = []

createdupdatedAt = str(datetime.datetime.now(timezone.utc))[
    :-9].replace(" ", "T") + "Z"
lastChangedAt = str(round(time.time() * 1000))
fechascan = time.strftime("%Y-%m-%d")


def subir_dynamodb(tabla_papeletas, papeletas, lista_id_query, lista_placa_query):
    cant_elementos = len(papeletas["entidad"])
    for x in range(cant_elementos):
        placa = papeletas["placa"][x]
        # id
        idx = lista_placa_query.index(placa)
        vehiculoID = lista_id_query[idx]
        match papeletas["entidad"][x]:
            case "SUTRAN":

                pr_sutran = {"PutRequest": {
                    "Item": {
                        "id": {"S": papeletas["numdocumento"][x] + papeletas["placa"][x]},
                        "agente_infractor": {"S": papeletas["agenteinfractor"][x]},
                        "clasificacion": {"S": papeletas["clasificacion"][x]},
                        "codigo_infraccion": {"S": papeletas["codigoinfraccion"][x]},
                        "correoenviado": {"BOOL": False},
                        "createdAt": {"S": createdupdatedAt},
                        "destinatarios_correoenviado": {"L": []},
                        "deuda_atu": {"NULL": True},
                        "deuda_ofisat": {"NULL": True},
                        "dscto_2": {"NULL": True},
                        "dscto_ofisat": {"NULL": True},
                        "entidad": {"S": "SUTRAN"},  # Fijo para SUTRAN
                        "estado_entidad": {"S": papeletas["estado"][x]},
                        # Este se puede dejar como valor default
                        "estado_mbr": {"S": "Pendiente de pago"},
                        "fechascan": {"S": papeletas["fechascan"][x]},
                        "fecha_correoenviado": {"NULL": True},
                        "fecha_documento": {"S": papeletas["fechadocumento"][x]},
                        "gast_cost": {"NULL": True},
                        "monto_infraccion": {"N": papeletas["montoinfraccion"][x]},
                        "monto_prontopago": {"N": papeletas["montoprontopago"][x]},
                        "nombre_infractor": {"S": papeletas["nombreinfractor"][x]},
                        "num_documento": {"S": papeletas["numdocumento"][x]},
                        "reglamento": {"NULL": True},
                        "tipo_documento": {"S": papeletas["tipodocumento"][x]},
                        # Igual al createdAt
                        "updatedAt": {"S": createdupdatedAt},
                        # Se puede cambiar el path para que contega el documento y la placa
                        "url_doc": {"S": papeletas["path_s3"][x]},
                        "url_docsextra": {"NULL": True},
                        "vehiculoID": {"S": vehiculoID},
                        "_lastChangedAt": {"N": lastChangedAt},
                        "_version": {"N": "1"},
                        "__typename": {"S": "Papeleta"}  # Fijo
                    }
                }}
                lista_write_sutran.append(pr_sutran)
            case "SAT LIMA":
                print("Todavía no se ha implementado SAT LIMA")
            case "CALLAO":
                print("Todavía no se ha implementado CALLAO")
            case other:
                print("No se ha detectado una entidad")
    # print(lista_write_sutran)
    resp_batch_write = client.batch_write_item(
        RequestItems={tabla_papeletas: lista_write_sutran})
    # print(resp_batch_write)

# response = client.batch_write_item(
#     RequestItems={
#         NOMBRE_TABLA_PAPELETAS: [
#             {
#                 'PutRequest': {
#                     'Item': {
#                         "id": {
#                             "S": "PYTHONTEST"
#                         },
#                         "correoenviado": {
#                             "BOOL": False
#                         },
#                         "createdAt": {
#                             "S": "2022-11-02T03:00:54.926Z"
#                         },
#                         "destinatarios_correoenviado": {
#                             "L": []
#                         },
#                         "entidad": {
#                             "S": "TEST"
#                         },
#                         "fechascan": {
#                             "S": "2022-11-01"
#                         },
#                         "fecha_correoenviado": {
#                             "NULL": True
#                         },
#                         "fecha_documento": {
#                             "S": "2022-11-01"
#                         },
#                         "num_documento": {
#                             "S": "PYTHONTESTBKD764"
#                         },
#                         "updatedAt": {
#                             "S": "2022-11-02T03:00:54.926Z"
#                         },
#                         "url_docsextra": {
#                             "M": {}
#                         },
#                         "vehiculoID": {
#                             "S": "0966621e-1cf8-4fa4-8924-8ccb4bed47a4"
#                         },
#                         "_lastChangedAt": {
#                             "N": "1667358054949"
#                         },
#                         "_version": {
#                             "N": "1"
#                         },
#                         "__typename": {
#                             "S": "Papeleta"
#                         }
#                     },
#                     "ConditionExpression": 'attribute_not_exists(num_documento)',
#                 },
#             },

#         ]
#     },

# )
# print(response)
