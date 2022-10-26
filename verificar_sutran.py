import requests
import urllib
import pandas as pd
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from pathlib import Path
from datetime import datetime
import logging
import boto3
from botocore.exceptions import ClientError
import os
from bs4 import BeautifulSoup

URL_SUTRAN_ORIGIN = "http://webexterno.sutran.gob.pe"
URL_SUTRAN_VERIFICAR_INFRACCION = "http://webexterno.sutran.gob.pe/GenerarTicket"


tipodocumento = "Papeletas Transito"
numdocumento = "2450068335"
fechadocumento = "21/10/2020"

# 15 Acta de Control para Servicios de Mercancias
# 14 Acta de Control para Servicios de Pasajeros
# 2 Formulario de infraccion
# 3 Materiales Peligrosos
# 4 Papeletas Transito

match tipodocumento:
    case "Acta de Control para Servicios de Mercancias":
        idTipoFormato = "15"
    case "Acta de Control para Servicios de Pasajeros":
        idTipoFormato = "14"
    case "Formulario de infraccion":
        idTipoFormato = "2"
    case "Materiales Peligrosos":
        idTipoFormato = "3"
    case "Papeletas Transito":
        idTipoFormato = "4"
    case _:
        idTipoFormato = "999"

payload_VerificarPapeleta = 'Ticket.IdInfractor=0&Ticket.IdTipoFormato=' + \
    idTipoFormato + '&Ticket.DocumentoInfraccion=' + numdocumento + \
    '&FechaInspeccion=' + urllib.parse.quote(fechadocumento, safe="")

headers_VerificarPapeleta = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '',
    'Origin': URL_SUTRAN_ORIGIN,
    'Referer': URL_SUTRAN_VERIFICAR_INFRACCION,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

resp_VerificarPapeleta = requests.request(
    "POST", URL_SUTRAN_VERIFICAR_INFRACCION, headers=headers_VerificarPapeleta, data=payload_VerificarPapeleta)
# print(resp_VerificarPapeleta.text)

doc_verificar = BeautifulSoup(resp_VerificarPapeleta.text, "html.parser")

# COLUMNAS NUEVAS
# 3 Agente Infractor
# 4 Nombre Infractor
# 5 Monto Infracción
# 6 Monto Pronto Pago
# 7 Estado


# Obviar el primer resultado (cabecera)
# tr_tags.pop(0)
class_tr_cabecera = "table-primary"
for tr in doc_verificar.find_all("tr", {"class": class_tr_cabecera}):
    tr.decompose()

# print(tr_tags)
lista_agenteinfractor = []
lista_nombreinfractor = []
lista_montoinfraccion = []
lista_montoprontopago = []
lista_estado = []

tr_tags = doc_verificar.find_all("tr")

for t in tr_tags:
    td = t.find_all("td")
    if td[7].text != "SIN ESTADO":
        lista_agenteinfractor.append(td[3].text)
        lista_nombreinfractor.append(td[4].text)
        lista_montoinfraccion.append(td[5].text)
        lista_montoprontopago.append(td[6].text)
        lista_estado.append(td[7].text)

dict_verificar = {"agenteinfractor": lista_agenteinfractor,
                  "nombreinfractor": lista_nombreinfractor,
                  "montoinfraccion": lista_montoinfraccion,
                  "montoprontopago": lista_montoprontopago,
                  "estado": lista_estado}

print(dict_verificar)
