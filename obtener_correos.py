import json
from graphqlclient import GraphQLClient

#GRAPHQL_ENDPOINT = 'https://mjga7yrhl5hvlbe5ypz6r27csu.appsync-api.us-east-1.amazonaws.com/graphql'
#API_KEY = "da2-rcfdc2v4ezezjgdubivb4qwhba"


def obtener_correos(cliente, endpoint, api_key):
    client = GraphQLClient(endpoint)
    client.inject_token(api_key, 'x-api-key')
    #lista_clientes = ["San Fernando", "Avgust"]
    # input_clientes = ''
    # for c in lista_clientes:
    #     input_clientes = input_clientes + '{ nombre: { eq: "' + c + '" } },'
    # input_clientes = input_clientes[:-1]
    queryClientes = """
  query MyQuery {
  listClientes(filter: {
    or: [
    { nombre: { eq: """ + '"' + cliente + '"' + """ } }
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
    q = client.execute(queryClientes)
    q = json.loads(q)
    # print(q["data"]["listClientes"]["items"])
    print(cliente)

    q = q["data"]["listClientes"]["items"]
    print(q)
    lista_correos = [q[0]["correo_supervisor"], q[0]["correo_comercial"]]

    return lista_correos


# obtener_correos(lista_clientes,GRAPHQL_ENDPOINT,API_KEY)
