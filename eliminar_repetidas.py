import boto3
from query_papeletas_graphql import query_papeletas
client = boto3.client("dynamodb")


def eliminar_repetidas(tabla_papeletas, dict_papeletas_scaneadas, endpoint, api_key):
    response_papeletas = query_papeletas(tabla_papeletas, endpoint, api_key)

    lista_papeletas_scaneadas = dict_papeletas_scaneadas["numdocumento"]
    lista_papeletas_existentes = []

    for p in response_papeletas["data"]["listPapeletas"]["items"]:
        lista_papeletas_existentes.append(p["num_documento"])

    s = set(lista_papeletas_existentes)
    lista_papeletas_nuevas = [
        x for x in lista_papeletas_scaneadas if x not in s]

    # Guardo los index de la lista de papeletas scaneadas

    lista_placa_nuevas = []
    lista_numdocumento_nuevas = []
    lista_tipodocumento_nuevas = []
    lista_fechadocumento_nuevas = []
    lista_codigoinfraccion_nuevas = []
    lista_clasificacion_nuevas = []
    lista_entidad_nuevas = []
    lista_fechascan_nuevas = []

    for n in lista_papeletas_nuevas:
        for s in lista_papeletas_scaneadas:
            if s == n:
                # Aquí obtengo el index de s
                idx = lista_papeletas_scaneadas.index(s)
                lista_placa_nuevas.append(
                    dict_papeletas_scaneadas["placa"][idx])
                lista_numdocumento_nuevas.append(
                    dict_papeletas_scaneadas["numdocumento"][idx])
                lista_tipodocumento_nuevas.append(
                    dict_papeletas_scaneadas["tipodocumento"][idx])
                lista_fechadocumento_nuevas.append(
                    dict_papeletas_scaneadas["fechadocumento"][idx])
                lista_codigoinfraccion_nuevas.append(
                    dict_papeletas_scaneadas["codigoinfraccion"][idx])
                lista_clasificacion_nuevas.append(
                    dict_papeletas_scaneadas["clasificacion"][idx])
                lista_entidad_nuevas.append(
                    dict_papeletas_scaneadas["entidad"][idx])
                lista_fechascan_nuevas.append(
                    dict_papeletas_scaneadas["fechascan"][idx])
                lista_fechascan_nuevas.append(
                    dict_papeletas_scaneadas["fechascan"][idx])

    dict_papeletas_nuevas = {
        "placa": lista_placa_nuevas,
        "numdocumento": lista_numdocumento_nuevas,
        "tipodocumento": lista_tipodocumento_nuevas,
        "fechadocumento": lista_fechadocumento_nuevas,
        "codigoinfraccion": lista_codigoinfraccion_nuevas,
        "clasificacion": lista_clasificacion_nuevas,
        "entidad": lista_entidad_nuevas,
        "fechascan": lista_fechascan_nuevas,

    }
    return dict_papeletas_nuevas
