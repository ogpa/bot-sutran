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


async def fetch(url, session):
    async with session.get(url) as response:
        await response.text()
        sessionid = extraer_string(
            response.headers["Set-Cookie"], "", "; path=/;")
        print(sessionid)


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def run(r):
    url = "http://webexterno.sutran.gob.pe/WebExterno/Pages/frmRecordInfracciones.aspx"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(3)
    # Create client session that will ensure we dont open new connection
    # per each request.
    async with aiohttp.ClientSession() as session:
        for i in range(r):
            # pass Semaphore and session to every GET request
            task = bound_fetch(sem, url, session)
            tasks.append(task)
        print(tasks)
        responses = asyncio.gather(*tasks)
        await responses

number = 20

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(number))
loop.run_until_complete(future)
