import requests
import urllib
from bs4 import BeautifulSoup
import asyncio
import aiohttp
URL_SUTRAN_ORIGIN = "http://webexterno.sutran.gob.pe"
URL_SUTRAN_HOME_INFRACCION = "http://webexterno.sutran.gob.pe/WebExterno/Pages/frmRecordInfracciones.aspx"


def extraer_string(textomaster, ini_cabecera, fin_cabecera):
    ini = textomaster.find(ini_cabecera)
    fin = textomaster.find(fin_cabecera, ini+len(ini_cabecera))
    texto = textomaster[ini+len(ini_cabecera):fin]
    return texto


lista_sessionid = []
lista_captcha = []
lista_viewstate = []
lista_viewstategenerator = []
lista_eventvalidation = []


async def query_ids(session: aiohttp.ClientSession):
    async with session.get(URL_SUTRAN_HOME_INFRACCION) as resp:

        data = (await resp.text())
        # print(data)

        sessionid = extraer_string(resp.headers["Set-Cookie"], "", "; path=/;")
        # print(sessionid)
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
    longitud_lista_placas = len(lista_placas)
    async with aiohttp.ClientSession() as session:
        tasks_ids = []
        for x in range(longitud_lista_placas):
            tasks_ids.append(query_ids(session=session))
        htmls_ids = await asyncio.gather(*tasks_ids, return_exceptions=True)


multi_placas = ["BLV785", "AVE847", "BDN910", "BKD764", "BEB884", "BEB741", "BHM942", "ATE776",
                "ATE778",
                "ATE880",
                "ATE914",
                "ATE937",
                "ATE938",
                "ATE939",
                "ATE940",
                "ATF713",
                "ATF714",
                "ATF715",
                "ATF716",
                "ATF720",
                "ATF730",
                "ATF747",
                "ATF748",
                "ATF749",
                "ATF752",
                "ATF761",
                "ATF762",
                "ATF763",
                "ATF765",
                "ATF777",
                "ATF789",
                "ATF790",
                "ATF791",
                "ATF792",
                "ATF837",
                "ATF841",
                "ATF842",
                "ATF843",
                "ATF845",
                "ATF855",
                "ATF884", "ATO907",
                "ATO910",
                "ATO912",
                "ATO916",
                "ATR722",
                "ATR727",
                "AUD787",
                "AUF752",
                "AXX086",
                "AXY076",
                "AXY114",
                "AXY116",
                "AXY222",
                "AXY562",
                "AXY563",
                "AXY577",
                "AXY590",
                "AXZ003",
                "AYJ274",
                "AYJ696",
                "AYK161",
                "AYK647",
                "AYL008",
                "AYL137",
                "AYL139",
                "AYL508",
                "AZD604",
                "AZK271",
                "AZK633",
                "AZM297",
                "BDC879",
                "BDC885",
                "BDD752",
                "BDD753",
                "BDD809",
                "BDD810",
                "BDD814",
                "BDD815",
                "BDD824",
                "BDD830",
                "BDD831",
                "BDD849",
                "BDD850",
                "BDD862",
                "BDD946",
                "BDE709",
                "BDE710",
                "BDE775",
                "BDE796",
                "BDE797",
                "BDE817",
                "BDF853",
                "BDF854",
                "BDF877",
                "BDF879",
                "BDF880",
                "BDG755",
                "BDG796",
                "BDG797",
                "BDG828",
                "BDG830",
                "BDG831",
                "BDG835",
                "BDG837",
                "BDG838",
                "BDG844"]
asyncio.run(mainids(multi_placas))
print(lista_sessionid)

lista_placa = []
lista_numdocumento = []
lista_tipodocumento = []
lista_fechadocumento = []
lista_codigoinfraccion = []
lista_clasificacion = []


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
            lista_placa.append(placa)
            lista_numdocumento.append(td[0].text)
            lista_tipodocumento.append(td[1].text)
            lista_fechadocumento.append(td[2].text)
            lista_codigoinfraccion.append(td[3].text)
            lista_clasificacion.append(td[4].text)


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

asyncio.run(main_datos(multi_placas, lista_sessionid, lista_captcha,
            lista_viewstate, lista_viewstategenerator, lista_eventvalidation))


dict_papeletas = {"placa": lista_placa,
                  "numdocumento": lista_numdocumento,
                  "tipodocumento": lista_tipodocumento,
                  "fechadocumento": lista_fechadocumento,
                  "codigoinfraccion": lista_codigoinfraccion,
                  "clasificacion": lista_clasificacion}

print(dict_papeletas)
# return dict_papeletas
# def obtener_datos_papeletas(lista_placas):
#     lista_placa = []
#     lista_numdocumento = []
#     lista_tipodocumento = []
#     lista_fechadocumento = []
#     lista_codigoinfraccion = []
#     lista_clasificacion = []
#     for p in lista_placas:
#         resp_HomeInfraccion = requests.request(
#             "GET", URL_SUTRAN_HOME_INFRACCION)
#         # print(resp_HomeInfraccion.headers)

#         session = extraer_string(
#             resp_HomeInfraccion.headers["Set-Cookie"], "", "; path=/;")
#         # print(session)

#         captcha = extraer_string(
#             resp_HomeInfraccion.text, 'scrolling="no" src="Captcha.aspx?numAleatorio=', '" width="')
#         # print(captcha)

#         viewstate = extraer_string(
#             resp_HomeInfraccion.text, 'name="__VIEWSTATE" id="__VIEWSTATE" value="', '" />')
#         # print(viewstate)

#         viewstategenerator = extraer_string(
#             resp_HomeInfraccion.text, 'name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="', '" />')
#         # print(viewstate)

#         eventvalidation = extraer_string(
#             resp_HomeInfraccion.text, 'name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="', '" />')
#         # print(eventvalidation)

#         payload_InfoPapeleta = '__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=' + urllib.parse.quote(viewstate, safe="") + '&__VIEWSTATEGENERATOR=' + viewstategenerator + '&__EVENTVALIDATION=' + urllib.parse.quote(
#             eventvalidation, safe="") + '&ddlTipoBusqueda=2&TxtBuscar=&txtPlaca=' + p + '&HFCodCapcha=&TxtCodImagen=' + captcha + '&BtnBuscar=Buscar&HdfModal2=&txtCorreo='
#         headers_InfoPapeleta = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'Accept-Language': 'en-US,en;q=0.9',
#             'Cache-Control': 'max-age=0',
#             'Connection': 'keep-alive',
#             'Content-Type': 'application/x-www-form-urlencoded',
#             'Cookie': session,
#             'Origin': URL_SUTRAN_ORIGIN,
#             'Referer': URL_SUTRAN_HOME_INFRACCION,
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
#         }

#         resp_InfoPapeleta = requests.request(
#             "POST", URL_SUTRAN_HOME_INFRACCION, headers=headers_InfoPapeleta, data=payload_InfoPapeleta)

#         # print(resp_InfoPapeleta.text)
#         doc = BeautifulSoup(resp_InfoPapeleta.text, "html.parser")
#         # tr_style_datospapeleta = "color:#333333;background-color:#F0F0F0;border-color:Silver;"
#         # tr_tags = doc.find_all("tr", {"style": tr_style_datospapeleta})
#         # print(tr_tags)

#         #id_table_datospapeleta = "gvDeudas"
#         #table_tags = doc.find_all("table", {"id": id_table_datospapeleta})

#         # print(table_tags)
#         # Placa
#         # 0 Número de documento
#         # 1 Tipo de Documento
#         # 2 Fecha de documento
#         # 3 Código de infracción
#         # 4 Clasificación
#         style_tr_datospapeleta_parcial = "border-color:Silver"

#         tr_tags = doc.find_all(
#             "tr", style=lambda tipo: tipo and style_tr_datospapeleta_parcial in tipo)
#         # print(tr_tags)

#         for t in tr_tags:
#             td = t.find_all("td")
#             lista_placa.append(p)
#             lista_numdocumento.append(td[0].text)
#             lista_tipodocumento.append(td[1].text)
#             lista_fechadocumento.append(td[2].text)
#             lista_codigoinfraccion.append(td[3].text)
#             lista_clasificacion.append(td[4].text)

#     dict_papeletas = {"placa": lista_placa,
#                       "numdocumento": lista_numdocumento,
#                       "tipodocumento": lista_tipodocumento,
#                       "fechadocumento": lista_fechadocumento,
#                       "codigoinfraccion": lista_codigoinfraccion,
#                       "clasificacion": lista_clasificacion}

#     # print(dict_papeletas)
#     return dict_papeletas
