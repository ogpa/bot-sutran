# modified fetch function with semaphore
import random
import asyncio
import aiohttp
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def extraer_string(textomaster, ini_cabecera, fin_cabecera):
    ini = textomaster.find(ini_cabecera)
    fin = textomaster.find(fin_cabecera, ini+len(ini_cabecera))
    texto = textomaster[ini+len(ini_cabecera):fin]
    return texto


async def fetch(limit):
    async with limit:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://webexterno.sutran.gob.pe/WebExterno/Pages/frmRecordInfracciones.aspx") as response:
                data = await response.text()
                sessionid = extraer_string(
                    response.headers["Set-Cookie"], "", "; path=/;")
                print(sessionid)


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def main(r):
    limit = asyncio.Semaphore(1)
    tasks = []
    # create instance of Semaphore

    # Create client session that will ensure we dont open new connection
    # per each request.
    for x in range(r):
        tasks.append(fetch(limit))
    results = await asyncio.gather(*tasks)
number = 60

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(main(number))
loop.run_until_complete(future)
