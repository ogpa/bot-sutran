import urllib
from bs4 import BeautifulSoup
import asyncio
import aiohttp
#from datetime import datetime
import datetime
URL_SUTRAN_ORIGIN = "http://webexterno.sutran.gob.pe"
URL_SUTRAN_HOME_INFRACCION = "http://webexterno.sutran.gob.pe/WebExterno/Pages/frmRecordInfracciones.aspx"
CANT_REQUESTS_PARALELO = 50


def extraer_string(textomaster, ini_cabecera, fin_cabecera):
    ini = textomaster.find(ini_cabecera)
    fin = textomaster.find(fin_cabecera, ini+len(ini_cabecera))
    texto = textomaster[ini+len(ini_cabecera):fin]
    return texto


def obtener_datos_papeletas(lista_placas):

    lista_sessionid = []
    lista_captcha = []
    lista_viewstate = []
    lista_viewstategenerator = []
    lista_eventvalidation = []

    # async def query_ids(session: aiohttp.ClientSession):
    async def query_ids(limite):
        async with limite:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL_SUTRAN_HOME_INFRACCION) as response:

                    data = (await response.text())
                    # print(data)

                    sessionid = extraer_string(
                        response.headers["Set-Cookie"], "", "; path=/;")
                    print(sessionid)
                    lista_sessionid.append(sessionid)

                    captcha = extraer_string(
                        data, 'scrolling="no" src="Captcha.aspx?numAleatorio=', '" width="')
                    # print(captcha)
                    lista_captcha.append(captcha)

                    viewstate = extraer_string(
                        data, 'name="__VIEWSTATE" id="__VIEWSTATE" value="', '" />')
                    # print(viewstate)
                    lista_viewstate.append(viewstate)

                    viewstategenerator = extraer_string(
                        data, 'name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="', '" />')
                    # print(viewstategenerator)
                    lista_viewstategenerator.append(viewstategenerator)

                    eventvalidation = extraer_string(
                        data, 'name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="', '" />')
                    # print(eventvalidation)
                    lista_eventvalidation.append(eventvalidation)

    async def mainids(lista_placas):
        limite = asyncio.Semaphore(CANT_REQUESTS_PARALELO)
        longitud_lista_placas = len(lista_placas)
        tasks_ids = []

        for x in range(longitud_lista_placas):
            tasks_ids.append(query_ids(limite))
        htmls_ids = await asyncio.gather(*tasks_ids, return_exceptions=True)

    # asyncio.run(mainids(lista_placas))

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(mainids(lista_placas))
    loop.run_until_complete(future)
    # print(lista_sessionid)

    lista_placa = []
    lista_numdocumento = []
    lista_tipodocumento = []
    lista_fechadocumento = []
    lista_codigoinfraccion = []
    lista_clasificacion = []
    lista_entidad = []
    lista_fechascan = []
    fecha_scan = datetime.datetime.today().strftime("%Y-%m-%d")

    async def query_datos(payload, sessionid, placa, session: aiohttp.ClientSession):
        headers_InfoPapeleta = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': sessionid,
            'Origin': URL_SUTRAN_ORIGIN,
            'Referer': URL_SUTRAN_HOME_INFRACCION,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        async with session.post(URL_SUTRAN_HOME_INFRACCION, data=payload, headers=headers_InfoPapeleta) as resp:

            resp_InfoPapeleta = (await resp.text())
            doc = BeautifulSoup(resp_InfoPapeleta, "html.parser")
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
                fecha = td[2].text
                fecha_doc = datetime.datetime.strptime(
                    fecha, '%d/%m/%Y').strftime('%Y-%m-%d')
                # print(fecha)
                # print(fecha_doc)

                lista_placa.append(placa)
                lista_numdocumento.append(td[0].text)
                lista_tipodocumento.append(td[1].text)
                # lista_fechadocumento.append(td[2].text)
                # Convierte la fecha de d/m/y a y-m-d
                lista_fechadocumento.append(fecha_doc)
                lista_codigoinfraccion.append(td[3].text)
                lista_clasificacion.append(td[4].text)
                lista_entidad.append("SUTRAN")
                lista_fechascan.append(fecha_scan)

    async def main_datos(multi_placas, lista_sessionid, lista_captcha, lista_viewstate, lista_viewstategenerator, lista_eventvalidation):
        longitud_lista_placas = len(lista_sessionid)
        async with aiohttp.ClientSession() as session:
            tasks_datos = []
            for x in range(longitud_lista_placas):
                payload = '__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=' + urllib.parse.quote(lista_viewstate[x], safe="") + '&__VIEWSTATEGENERATOR=' + lista_viewstategenerator[x] + '&__EVENTVALIDATION=' + urllib.parse.quote(
                    lista_eventvalidation[x], safe="") + '&ddlTipoBusqueda=2&TxtBuscar=&txtPlaca=' + multi_placas[x] + '&HFCodCapcha=&TxtCodImagen=' + lista_captcha[x] + '&BtnBuscar=Buscar&HdfModal2=&txtCorreo='
                tasks_datos.append(query_datos(
                    payload, lista_sessionid[x], multi_placas[x], session=session))
            htmls_datos = await asyncio.gather(*tasks_datos, return_exceptions=True)

    asyncio.run(main_datos(lista_placas, lista_sessionid, lista_captcha,
                lista_viewstate, lista_viewstategenerator, lista_eventvalidation))

    dict_papeletas = {"placa": lista_placa,
                      "numdocumento": lista_numdocumento,
                      "tipodocumento": lista_tipodocumento,
                      "fechadocumento": lista_fechadocumento,
                      "codigoinfraccion": lista_codigoinfraccion,
                      "clasificacion": lista_clasificacion,
                      "entidad": lista_entidad,
                      "fechascan": lista_fechascan}

    # print(dict_papeletas)
    return dict_papeletas
