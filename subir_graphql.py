from graphqlclient import GraphQLClient
from datetime import datetime

query = """
mutation operation($input: CreatePapeletaInput!) {
  createPapeleta(input: $input) {
    id
    num_documento
    fecha_documento
    codigo_infraccion
    monto_infraccion
    monto_prontopago
    estado_entidad
    url_doc
    url_docsextra
    reglamento
    gast_cost
    dscto_2
    dscto_ofisat
    dscto_webbancos
    deuda_ofisat
    deuda_atu
    licencia_conducir
    tipo_docidentidad
    docidentidad
    tipo_documento
    clasificacion
    agente_infractor
    nombre_infractor
    entidad
    fechascan
    correoenviado
    fecha_correoenviado
    hora_correoenviado
    destinatarios_correoenviado
    horascan
    vehiculoID
    estado_mbr
    fecha_infraccion
    hora_infraccion
    cliente
    placa
    createdAt
    updatedAt
    _version
    _lastChangedAt
    _deleted
  }
}
"""


def convertir_lista_a_str(lista):
    texto = ""

    for e in lista:
        texto = texto + '"' + e + '"' + ","
    return texto[:-1]


def subir_graphql(tabla_papeletas, papeletas, lista_id_query, lista_placa_query, endpoint, api_key):
    client = GraphQLClient(endpoint)
    client.inject_token(api_key, 'x-api-key')
    cant_elementos = len(papeletas["entidad"])
    for x in range(cant_elementos):
        placa = papeletas["placa"][x]
        # id
        idx = lista_placa_query.index(placa)
        vehiculoID = lista_id_query[idx]
        #cliente = lista_cliente_query[idx]
        hora = datetime.now().time()
        hora = str(hora)
        hora = hora[:-3]
        match papeletas["entidad"][x]:
            case "SUTRAN":
                d_c = convertir_lista_a_str(
                    papeletas["destinatarios_correoenviado"][x])
                variables = """{
  "input": {
    "id": """ + '"' + papeletas["numdocumento"][x] + papeletas["placa"][x] + '"' + """,
    "agente_infractor": """ + '"' + papeletas["agenteinfractor"][x] + '"' + """,
    "clasificacion": """ + '"' + papeletas["clasificacion"][x] + '"' + """,
    "cliente": """ + '"' + papeletas["cliente"][x] + '"' + """,
    "codigo_infraccion": """ + '"' + papeletas["codigoinfraccion"][x] + '"' + """,
    "correoenviado": true,
    "destinatarios_correoenviado": [""" + d_c + """],
    "entidad": "SUTRAN",
    "estado_entidad": """ + '"' + papeletas["estado"][x] + '"' + """,
    "estado_mbr": "Pendiente de pago",
    "fechascan": """ + '"' + papeletas["fechascan"][x] + '"' + """,
    "fecha_documento": """ + '"' + papeletas["fechadocumento"][x] + '"' + """,
    "fecha_infraccion": """ + '"' + papeletas["fechadocumento"][x] + '"' + """,
    "horascan": """ + '"' + hora + '"' + """,
    "infractor": """ + '"' + papeletas["cliente"][x] + '"' + """,
    "monto_infraccion": """ + papeletas["montoinfraccion"][x] + """, 
    "monto_prontopago": """ + papeletas["montoprontopago"][x] + """,
    "nombre_infractor": """ + '"' + papeletas["nombreinfractor"][x] + '"' + """,
    "num_documento": """ + '"' + papeletas["numdocumento"][x] + '"' + """,
    "placa":  """ + '"' + papeletas["placa"][x] + '"' + """,
    "tipo_documento": """ + '"' + papeletas["tipodocumento"][x] + '"' + """,
    "url_doc": """ + '"' + papeletas["path_s3"][x] + '"' + """,
    "vehiculoID": """ + '"' + vehiculoID + '"' + """
  }
}"""
                # print(variables)
                r = client.execute(query, variables)
                # print(r)

                # pr_sutran = {"PutRequest": {
                #     "Item": {
                #         "id": {"S": papeletas["numdocumento"][x] + papeletas["placa"][x]},
                #         "agente_infractor": {"S": papeletas["agenteinfractor"][x]},
                #         "clasificacion": {"S": papeletas["clasificacion"][x]},
                #         "codigo_infraccion": {"S": papeletas["codigoinfraccion"][x]},
                #         "correoenviado": {"BOOL": False},
                #         "createdAt": {"S": createdupdatedAt},
                #         "destinatarios_correoenviado": {"L": []},
                #         "deuda_atu": {"NULL": True},
                #         "deuda_ofisat": {"NULL": True},
                #         "docidentidad": {"NULL": True},
                #         "dscto_2": {"NULL": True},
                #         "dscto_ofisat": {"NULL": True},
                #         "dscto_webbancos": {"NULL": True},
                #         "entidad": {"S": "SUTRAN"},  # Fijo para SUTRAN
                #         "estado_entidad": {"S": papeletas["estado"][x]},
                #         # Este se puede dejar como valor default
                #         "estado_mbr": {"S": "Pendiente de pago"},
                #         "fechascan": {"S": papeletas["fechascan"][x]},
                #         "fecha_correoenviado": {"NULL": True},
                #         "hora_correoenviado": {"NULL": True},
                #         "horascan": {"NULL": True},
                #         "fecha_documento": {"S": papeletas["fechadocumento"][x]},
                #         "gast_cost": {"NULL": True},
                #         "licencia_conducir": {"NULL": True},
                #         "monto_infraccion": {"N": papeletas["montoinfraccion"][x]},
                #         "monto_prontopago": {"N": papeletas["montoprontopago"][x]},
                #         "nombre_infractor": {"S": papeletas["nombreinfractor"][x]},
                #         "num_documento": {"S": papeletas["numdocumento"][x]},
                #         "reglamento": {"NULL": True},
                #         "tipo_docidentidad": {"NULL": True},
                #         "tipo_documento": {"S": papeletas["tipodocumento"][x]},
                #         # Igual al createdAt
                #         "updatedAt": {"S": createdupdatedAt},
                #         # Se puede cambiar el path para que contega el documento y la placa
                #         "url_doc": {"S": papeletas["path_s3"][x]},
                #         "url_docsextra": {"NULL": True},
                #         "vehiculoID": {"S": vehiculoID},
                #         "_lastChangedAt": {"N": lastChangedAt},
                #         "_version": {"N": "1"},
                #         "__typename": {"S": "Papeleta"},  # Fijo
                #         "_deleted": {"BOOL": False}
                #     }
                # }}
                # lista_write_sutran.append(pr_sutran)
            case "SAT LIMA":
                print("Todavía no se ha implementado SAT LIMA")
            case "CALLAO":
                print("Todavía no se ha implementado CALLAO")
            case other:
                print("No se ha detectado una entidad")
    # print(lista_write_sutran)
    # resp_batch_write = client.batch_write_item(
    #     RequestItems={tabla_papeletas: lista_write_sutran})
    # print(resp_batch_write)
