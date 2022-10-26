
import urllib
import asyncio
import aiohttp
from bs4 import BeautifulSoup

URL_SUTRAN_ORIGIN = "http://webexterno.sutran.gob.pe"
URL_SUTRAN_VERIFICAR_INFRACCION = "http://webexterno.sutran.gob.pe/GenerarTicket"


# Necesita tipodocumento, numdocumento y fechadocumento del dictionary listapapeletas
def verificar_papeletas(papeletas):
    

    #longitud_listas = len(numdocumento)
    lista_numdocumento=[]
    lista_agenteinfractor = []
    lista_nombreinfractor = []
    lista_montoinfraccion = []
    lista_montoprontopago = []
    lista_estado = []

    async def query_verificar(payload,numdocumento,session: aiohttp.ClientSession):


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
        async with session.post(URL_SUTRAN_VERIFICAR_INFRACCION,data=payload,headers=headers_VerificarPapeleta) as resp:

            resp_VerificarPapeleta = (await resp.text())
            # print(data)

            doc_verificar = BeautifulSoup(
            resp_VerificarPapeleta, "html.parser")

            # COLUMNAS NUEVAS
            # 3 Agente Infractor
            # 4 Nombre Infractor
            # 5 Monto Infracción
            # 6 Monto Pronto Pago
            # 7 Estado

            # Obviar el primer resultado (cabecera)
         
            class_tr_cabecera = "table-primary"
            for tr in doc_verificar.find_all("tr", {"class": class_tr_cabecera}):
                tr.decompose()

            # print(tr_tags)

            tr_tags = doc_verificar.find_all("tr")

            for t in tr_tags:
                td = t.find_all("td")
                if td[7].text != "SIN ESTADO":
                    lista_numdocumento.append(numdocumento)
                    lista_agenteinfractor.append(td[3].text)
                    lista_nombreinfractor.append(td[4].text)
                    lista_montoinfraccion.append(td[5].text)
                    lista_montoprontopago.append(td[6].text)
                    lista_estado.append(td[7].text)


    async def main_verificar(papeletas):
        numdocumento = papeletas["numdocumento"]
        tipodocumento = papeletas["tipodocumento"]
        fechadocumento = papeletas["fechadocumento"]
        longitud_lista_papeletas = len(numdocumento)
        
        async with aiohttp.ClientSession() as session:

            tasks_verificar = []

            for x in range(longitud_lista_papeletas):

                match tipodocumento[x]:
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

                payload = 'Ticket.IdInfractor=0&Ticket.IdTipoFormato=' + \
                idTipoFormato + '&Ticket.DocumentoInfraccion=' + numdocumento[x] + \
                '&FechaInspeccion=' + \
                urllib.parse.quote(fechadocumento[x], safe="")

                tasks_verificar.append(query_verificar(payload,numdocumento[x],session=session))

            htmls_verificar = await asyncio.gather(*tasks_verificar, return_exceptions=True)


    asyncio.run(main_verificar(papeletas))

    dict_verificar = {"numdocumento":lista_numdocumento,
                        "agenteinfractor": lista_agenteinfractor,
                      "nombreinfractor": lista_nombreinfractor,
                      "montoinfraccion": lista_montoinfraccion,
                      "montoprontopago": lista_montoprontopago,
                      "estado": lista_estado}

    return dict_verificar
