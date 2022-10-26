import urllib
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from datetime import datetime
import base64
URL_SUTRAN_ORIGIN = "http://webexterno.sutran.gob.pe"
URL_SUTRAN_CINEMOMETRO = "https://webexterno.sutran.gob.pe/WebExterno/Pages/frmPapeletasCinemometro.aspx"
RUC_MB_RENTING = "20605414410"

def extraer_string(textomaster, ini_cabecera, fin_cabecera):
    ini = textomaster.find(ini_cabecera)
    fin = textomaster.find(fin_cabecera, ini+len(ini_cabecera))
    texto = textomaster[ini+len(ini_cabecera):fin]
    return texto

def obtener_fotos(papeletas):
    
    lista_sessionid = []
    lista_captcha = []
    lista_viewstate = []
    lista_viewstategenerator = []
    lista_eventvalidation = []


    async def query_ids(session: aiohttp.ClientSession):
        async with session.get(URL_SUTRAN_CINEMOMETRO) as resp:

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


    async def mainids(papeletas):
        numdocumento = papeletas["numdocumento"]

        longitud_lista_papeletas = len(numdocumento)
        async with aiohttp.ClientSession() as session:
            tasks_ids = []
            for x in range(longitud_lista_papeletas):
                tasks_ids.append(query_ids(session=session))
            htmls_ids = await asyncio.gather(*tasks_ids, return_exceptions=True)


    asyncio.run(mainids(papeletas))
    #print(lista_sessionid)
    
    
    lista_numdocumento = []
    lista_verfoto = []
    lista_viewstate_datos = []
    lista_viewstategenerator_datos=[]
    lista_eventvalidation_datos=[]
    lista_numdocumento_datos = []

    async def query_datos(payload, sessionid, numdocumento, session: aiohttp.ClientSession):
        headers_Datos = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'en',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': sessionid,
  'Origin': URL_SUTRAN_ORIGIN,
  'Referer': URL_SUTRAN_CINEMOMETRO,
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}
        async with session.post(URL_SUTRAN_CINEMOMETRO, data=payload, headers=headers_Datos) as resp:

            resp_InfoPapeleta = (await resp.text())
            # doc = BeautifulSoup(resp_InfoPapeleta, "html.parser")
            # # print(table_tags)
            # # Placa
            # # 0 Número de documento
            # # 1 Tipo de Documento
            # # 2 Fecha de documento
            # # 3 Código de infracción
            # # 4 Clasificación
            # style_tr_datospapeleta_parcial = "color:#333333;background-color:#F0F0F0;border-color:Silver;"

            # tr_tags = doc.find_all(
            #     "tr", style=lambda tipo: tipo and style_tr_datospapeleta_parcial in tipo)
            # # print(tr_tags)

            # for t in tr_tags:
            #     td = t.find_all("td")
                
            #     lista_numdocumento.append(td[0].text)
            #     lista_verfoto.append(td[8].text)
            
            # sessionid = extraer_string(resp.headers["Set-Cookie"], "", "; path=/;")
            # # print(sessionid)
            # lista_sessionid.append(sessionid)

            # captcha = extraer_string(
            #     resp_InfoPapeleta, 'scrolling="no" src="Captcha.aspx?numAleatorio=', '" width="')
            # # print(captcha)
            # lista_captcha.append(captcha)

            viewstate = extraer_string(
                resp_InfoPapeleta, 'name="__VIEWSTATE" id="__VIEWSTATE" value="', '" />')
            # print(viewstate)
            lista_viewstate_datos.append(viewstate)

            viewstategenerator = extraer_string(
                resp_InfoPapeleta, 'name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="', '" />')
            # print(viewstategenerator)
            lista_viewstategenerator_datos.append(viewstategenerator)

            eventvalidation = extraer_string(
                resp_InfoPapeleta, 'name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="', '" />')
            # print(eventvalidation)
            lista_eventvalidation_datos.append(eventvalidation)
            lista_numdocumento_datos.append(numdocumento)
                

    async def main_datos(papeletas, lista_sessionid, lista_captcha, lista_viewstate, lista_viewstategenerator, lista_eventvalidation):
        numdocumento = papeletas["numdocumento"]
        longitud_lista_placas = len(lista_sessionid)
        async with aiohttp.ClientSession() as session:
            tasks_datos = []
            for x in range(longitud_lista_placas):
                payload='__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE='+ urllib.parse.quote(lista_viewstate[x], safe="") + '&__VIEWSTATEGENERATOR='+ lista_viewstategenerator[x] +'&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION='+ urllib.parse.quote(lista_eventvalidation[x], safe="") +'&rbtListMovimiento=A&txtActa=' + numdocumento[x] + '&ddlTipoBusqueda=3&TxtBuscar=' + RUC_MB_RENTING +'&txtPlaca=&HFCodCapcha=&TxtCodImagen=' +lista_captcha[x] + '&BtnBuscar=Buscar&HfNumAleatorioAcceso=&HiddenField2=&tipobusqueda1=rbtRecogerSutran1'
                tasks_datos.append(query_datos(
                    payload, lista_sessionid[x], numdocumento[x], session=session))
            htmls_datos = await asyncio.gather(*tasks_datos, return_exceptions=True)

    asyncio.run(main_datos(papeletas, lista_sessionid, lista_captcha,
                lista_viewstate, lista_viewstategenerator, lista_eventvalidation))


    lista_src=[]
    lista_numdocumentofotos=[]
    async def query_fotos(payload, numdocumento, session: aiohttp.ClientSession):
        headers_Fotos = {
  'Accept': '*/*',
  'Accept-Language': 'en',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': URL_SUTRAN_ORIGIN,
  'Referer': URL_SUTRAN_CINEMOMETRO,
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
  'X-MicrosoftAjax': 'Delta=true',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
}
        async with session.post(URL_SUTRAN_CINEMOMETRO, data=payload, headers=headers_Fotos) as resp:

            resp_Fotos = (await resp.text())

            #Obtener src de fotos

            src= extraer_string(
                resp_Fotos, 'class="css_image1" src="data:image/jpg;base64,', '" src="%20"')
            #lista_src.append(src)
            src_encode = src.encode()
            with open(numdocumento + ".jpg", "wb") as fh:
                fh.write(base64.decodebytes(src_encode))
            
            lista_numdocumentofotos.append(numdocumento)
            
            
                

    async def main_fotos(lista_numdocumento_datos, lista_viewstate_datos, lista_viewstategenerator_datos,lista_eventvalidation_datos):
        
        longitud_lista_papeletas = len(lista_numdocumento_datos)
        async with aiohttp.ClientSession() as session:
            tasks_fotos = []
            for x in range(longitud_lista_papeletas):
                #payload='__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE='+ urllib.parse.quote(lista_viewstate[x], safe="") + '&__VIEWSTATEGENERATOR='+ lista_viewstategenerator[x] +'&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION='+ urllib.parse.quote(lista_eventvalidation[x], safe="") +'&rbtListMovimiento=A&txtActa=' + numdocumento[x] + '&ddlTipoBusqueda=3&TxtBuscar=' + RUC_MB_RENTING +'&txtPlaca=&HFCodCapcha=&TxtCodImagen=' +lista_captcha[x] + '&BtnBuscar=Buscar&HfNumAleatorioAcceso=&HiddenField2=&tipobusqueda1=rbtRecogerSutran1'
                payload = 'ScriptManager1=UPDModal%7CgvCinemometro%24ctl02%24btnVer&__LASTFOCUS=&__EVENTTARGET=gvCinemometro%24ctl02%24btnVer&__EVENTARGUMENT=&__VIEWSTATE='+ urllib.parse.quote(lista_viewstate_datos[x], safe="") +'&__VIEWSTATEGENERATOR=' + lista_viewstategenerator_datos[x] + '&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION=' + urllib.parse.quote(lista_eventvalidation_datos[x], safe="") +'&rbtListMovimiento=A&txtActa=&ddlTipoBusqueda=2&TxtBuscar=&txtPlaca=&HFCodCapcha=&TxtCodImagen=&HfNumAleatorioAcceso=&HiddenField2=&tipobusqueda1=rbtRecogerSutran1&__ASYNCPOST=true&'
                tasks_fotos.append(query_fotos(
                    payload, lista_numdocumento_datos[x], session=session))
            htmls_fotos = await asyncio.gather(*tasks_fotos, return_exceptions=True)

    # lista_numdocumento = []
    # lista_verfoto = []
    # lista_viewstate_datos = []
    # lista_viewstategenerator_datos=[]
    # lista_eventvalidation_datos=[]
    # lista_numdocumento_datos = []

    asyncio.run(main_fotos(lista_numdocumento_datos, lista_viewstate_datos, lista_viewstategenerator_datos,
                lista_eventvalidation_datos))

    dict_datosfotos = {
                    "numdocumento": lista_numdocumentofotos,
                    
                    "src":lista_src}

    #print(dict_papeletas)
    return dict_datosfotos