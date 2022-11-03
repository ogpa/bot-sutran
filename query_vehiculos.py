import requests
from bs4 import BeautifulSoup
import pandas as pd
import boto3

client = boto3.client("dynamodb")

#tabla_vehiculos = "Vehiculo-lantl5egqfformu4wl5ale7p6e-dev"

# Se deben obviar los que tengan _deleted = true


def query_vehiculos(tabla_vehiculos):
    response_vehiculos = client.scan(
        TableName=tabla_vehiculos,
        ProjectionExpression='#i,#p,#c,#d',
        ExpressionAttributeNames={
            "#i": "id",
            "#p": "placa",
            "#c": "clienteID",
            "#d": "_deleted"},
        FilterExpression='#d <> :d',
        ExpressionAttributeValues={":d": {"BOOL": True}}

    )
    # print(response_vehiculos["Items"])
    return (response_vehiculos["Items"])


# query_vehiculos(tabla_vehiculos)
