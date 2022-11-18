import requests
import json
import pandas as pd
from graphqlclient import GraphQLClient

GRAPHQL_ENDPOINT = 'https://mjga7yrhl5hvlbe5ypz6r27csu.appsync-api.us-east-1.amazonaws.com/graphql'
API_KEY = "da2-rcfdc2v4ezezjgdubivb4qwhba"
client = GraphQLClient(GRAPHQL_ENDPOINT)
client.inject_token(API_KEY, 'x-api-key')
mutation = """
  mutation add {
    createPapeleta(
      input:{
      id: "TEST"
      num_documento: "2111111450"
      entidad: "SUTRAN"
      fechascan: "2022-11-03"
      vehiculoID: "bf3f20b6-66e7-459d-ba7d-38adfd540c58"
      destinatarios_correoenviado: null
    }
    ) {
      id
      num_documento
      createdAt
      entidad
      fechascan
    }
  }
"""
quer1 = """
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
    createdAt
    updatedAt
    _version
    _lastChangedAt
    _deleted
  }
}


"""
queryFiltradoDeleted = """
  query MyQuery {
  listPapeletas(filter:{
    _deleted:null
  }) {
    items {
      id
      fecha_documento
      _deleted
    }
  }
}
"""
query = """
  query MyQuery {
  listPapeletas {
    items {
      id
      fecha_documento
      _deleted
    }
  }
}
"""

queryPapeletas = """
  query MyQuery {
  listPapeletas {
    items {
      id
      num_documento
      _deleted
    }
  }
}
"""

fecha = "2022-11-09"
queryVehiculos = """
  query MyQuery {
  listVehiculos(filter:{
    v_cliente:{
      eq: "v0_cliente"
    }
  }) {
    items {
      placa
      cliente
      id
    }
  }
}
"""

lista_clientes = ["San Fernando", "Avgust"]
input_clientes = ''
for c in lista_clientes:
    input_clientes = input_clientes + '{ nombre: { eq: "' + c + '" } },'

input_clientes = input_clientes[:-1]
queryClientes = """
  query MyQuery {
  listClientes(filter: {
    or: [
    """ + input_clientes+"""
    ],
    and:[
       { v_supervisor: { eq: "v0_supervisor" } }
    ]
  }) {
    items {
      correo_supervisor
      correo_comercial
      nombre
    }
  }
}
"""

variables1 = """{
  "input": {
    "id": "DOS",
    "num_documento": "DOS",
    "fecha_documento": null,
    "entidad": "SUTRAN",
    "fechascan": """ + '"' + fecha + '"' + """,
    "correoenviado": false,
    "fecha_correoenviado": null,
    "destinatarios_correoenviado": [],
    "vehiculoID": "0966621e-1cf8-4fa4-8924-8ccb4bed47a4"
  }
}"""

variablesquery = """{
  "input": {
    "_deleted":true
  }
}"""
# print(variables1)
#m = client.execute(quer1, variables1)
# print(m)
# print(variables1)

# Query papeletas
q = client.execute(queryClientes)
q = json.loads(q)
# print(type(q))
print(q)

# Filtro los que tienen _deleted: null
# q_filtrado = []

# for p in q["data"]["listPapeletas"]["items"]:
#     if p["_deleted"] == None:
#         q_filtrado.append(p["id"])

# print(q_filtrado)
