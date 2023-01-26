import json
from graphqlclient import GraphQLClient


#tabla_vehiculos = "Vehiculo-lantl5egqfformu4wl5ale7p6e-dev"
#endpoint = "https://mjga7yrhl5hvlbe5ypz6r27csu.appsync-api.us-east-1.amazonaws.com/graphql"
#api_key = "da2-rcfdc2v4ezezjgdubivb4qwhba"
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
