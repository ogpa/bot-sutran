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
URL_SUTRAN_HOME_INFRACCION = "http://webexterno.sutran.gob.pe/WebExterno/Pages/frmRecordInfracciones.aspx"


def extraer_string(textomaster, ini_cabecera, fin_cabecera):
    ini = textomaster.find(ini_cabecera)
    fin = textomaster.find(fin_cabecera, ini+len(ini_cabecera))
    texto = textomaster[ini+len(ini_cabecera):fin]
    return texto


def obtener_datos_papeletas(lista_placas):
    lista_placa = []
    lista_numdocumento = []
    lista_tipodocumento = []
    lista_fechadocumento = []
    lista_codigoinfraccion = []
    lista_clasificacion = []
    for p in lista_placas:
        resp_HomeInfraccion = requests.request(
            "GET", URL_SUTRAN_HOME_INFRACCION)
        # print(resp_HomeInfraccion.headers)

        session = extraer_string(
            resp_HomeInfraccion.headers["Set-Cookie"], "", "; path=/;")
        # print(session)

        captcha = extraer_string(
            resp_HomeInfraccion.text, 'scrolling="no" src="Captcha.aspx?numAleatorio=', '" width="')
        # print(captcha)

        viewstate = extraer_string(
            resp_HomeInfraccion.text, 'name="__VIEWSTATE" id="__VIEWSTATE" value="', '" />')
        # print(viewstate)

        viewstategenerator = extraer_string(
            resp_HomeInfraccion.text, 'name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="', '" />')
        # print(viewstate)

        eventvalidation = extraer_string(
            resp_HomeInfraccion.text, 'name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="', '" />')
        # print(eventvalidation)

        payload_InfoPapeleta = '__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=' + urllib.parse.quote(viewstate, safe="") + '&__VIEWSTATEGENERATOR=' + viewstategenerator + '&__EVENTVALIDATION=' + urllib.parse.quote(
            eventvalidation, safe="") + '&ddlTipoBusqueda=2&TxtBuscar=&txtPlaca=' + p + '&HFCodCapcha=&TxtCodImagen=' + captcha + '&BtnBuscar=Buscar&HdfModal2=&txtCorreo='
        headers_InfoPapeleta = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': session,
            'Origin': URL_SUTRAN_ORIGIN,
            'Referer': URL_SUTRAN_HOME_INFRACCION,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }

        resp_InfoPapeleta = requests.request(
            "POST", URL_SUTRAN_HOME_INFRACCION, headers=headers_InfoPapeleta, data=payload_InfoPapeleta)

        # print(resp_InfoPapeleta.text)
        doc = BeautifulSoup(resp_InfoPapeleta.text, "html.parser")
        # tr_style_datospapeleta = "color:#333333;background-color:#F0F0F0;border-color:Silver;"
        # tr_tags = doc.find_all("tr", {"style": tr_style_datospapeleta})
        # print(tr_tags)

        #id_table_datospapeleta = "gvDeudas"
        #table_tags = doc.find_all("table", {"id": id_table_datospapeleta})

        # print(table_tags)
        # Placa
        # 0 Número de documento
        # 1 Tipo de Documento
        # 2 Fecha de documento
        # 3 Código de infracción
        # 4 Clasificación
        style_tr_datospapeleta_parcial = "border-color:Silver"

        tr_tags = doc.find_all(
            "tr", style=lambda tipo: tipo and style_tr_datospapeleta_parcial in tipo)
        # print(tr_tags)

        for t in tr_tags:
            td = t.find_all("td")
            lista_placa.append(p)
            lista_numdocumento.append(td[0].text)
            lista_tipodocumento.append(td[1].text)
            lista_fechadocumento.append(td[2].text)
            lista_codigoinfraccion.append(td[3].text)
            lista_clasificacion.append(td[4].text)

    dict_papeletas = {"placa": lista_placa,
                      "numdocumento": lista_numdocumento,
                      "tipodocumento": lista_tipodocumento,
                      "fechadocumento": lista_fechadocumento,
                      "codigoinfraccion": lista_codigoinfraccion,
                      "clasificacion": lista_clasificacion}

    # print(dict_papeletas)
    return dict_papeletas
