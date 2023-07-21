import json
from graphqlclient import GraphQLClient


# Se deben obviar los que tengan _deleted = true


def query_vehiculos(tabla_vehiculos, endpoint, api_key):
    client = GraphQLClient(endpoint)
    client.inject_token(api_key, 'x-api-key')
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
    q = client.execute(queryVehiculos)
    q = json.loads(q)
    # print(q)
    return q["data"]["listVehiculos"]["items"]


#query_vehiculos(tabla_vehiculos, endpoint, api_key)
