from graphqlclient import GraphQLClient

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
    latitud_infraccion
    longitud_infraccion
    fecha_infraccion
    hora_infraccion
    placa
    cliente
    infractor
    fecha_pago
    cont_pago
    url_doc_pago
    estado_json
    estado_actual
    createdAt
    updatedAt
    estado_mbr
    _version
    _lastChangedAt
    _deleted
  }
}
"""
# [\"{\\\"Pendiente\\\":\\\"hola\\\"}\"]
fecha = "2023-01-25"
url = "public/ABC123/Papeletas/245012/Papeleta_245012.jpg"
variables = """{
  "input": {
        "id": "v2",
        "num_documento": "logapiqw",
        "url_docsextra": "{}",
        "estado_json": \"{\\\"Pendiente\\\":{\\\"fecha_inicio\\\":\\\"""" + fecha + """\\\",\\\"url_doc\\\":\\\"""" + url + """\\\"}}\",
        "entidad": "SUTRAN",
        "fechascan": "2023-01-24",
        "correoenviado": false,
        "destinatarios_correoenviado": [],
        "vehiculoID": "1ad8c0b3-31bd-4354-85c4-a014399b4db3",
        "estado_mbr":"Pendiente"
    }
}"""

client = GraphQLClient(
    "https://mjga7yrhl5hvlbe5ypz6r27csu.appsync-api.us-east-1.amazonaws.com/graphql")
client.inject_token("da2-rcfdc2v4ezezjgdubivb4qwhba", 'x-api-key')

r = client.execute(query, variables)
print(r)
