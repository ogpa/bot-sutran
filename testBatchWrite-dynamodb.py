import requests
from bs4 import BeautifulSoup
import pandas as pd
import boto3
import time

lastChangedAt = str(int(time.time()))


client = boto3.client("dynamodb")

NOMBRE_TABLA_PAPELETAS = "Papeleta-lantl5egqfformu4wl5ale7p6e-dev"

# 0966621e-1cf8-4fa4-8924-8ccb4bed47a4 es el id de la BKD764
# CREAR UN DICCCIONARIO PARA QUE SEA MÁS FÁCIL
response = client.batch_write_item(
    RequestItems={
        NOMBRE_TABLA_PAPELETAS: [
            {
                'PutRequest': {
                    'Item': {
                        "id": {
                            "S": "PYTHONTEST"
                        },
                        "correoenviado": {
                            "BOOL": False
                        },
                        "createdAt": {
                            "S": "2022-11-02T03:00:54.926Z"
                        },
                        "destinatarios_correoenviado": {
                            "L": []
                        },
                        "entidad": {
                            "S": "TEST"
                        },
                        "fechascan": {
                            "S": "2022-11-01"
                        },
                        "fecha_correoenviado": {
                            "NULL": True
                        },
                        "fecha_documento": {
                            "S": "2022-11-01"
                        },
                        "num_documento": {
                            "S": "PYTHONTESTBKD764"
                        },
                        "updatedAt": {
                            "S": "2022-11-02T03:00:54.926Z"
                        },
                        "url_docsextra": {
                            "M": {}
                        },
                        "vehiculoID": {
                            "S": "0966621e-1cf8-4fa4-8924-8ccb4bed47a4"
                        },
                        "_lastChangedAt": {
                            "N": "1667358054949"
                        },
                        "_version": {
                            "N": "1"
                        },
                        "__typename": {
                            "S": "Papeleta"
                        }
                    }
                },
            },
        ]
    },

)
print(response)
