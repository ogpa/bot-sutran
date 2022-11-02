import requests
from bs4 import BeautifulSoup
import pandas as pd
import boto3
NOMBRE_TABLA_VEHICULOS = "Vehiculo-lantl5egqfformu4wl5ale7p6e-dev"
client = boto3.client("dynamodb")
response = client.scan(
    TableName=NOMBRE_TABLA_VEHICULOS,
    ProjectionExpression='placa,clienteID',

)

# placas
lista_placa = []
lista_clienteID = []
for i in response["Items"]:
    lista_placa.append(i["placa"]["S"])
    lista_clienteID.append(i["clienteID"]["S"])

print(lista_placa)
print(lista_clienteID)
