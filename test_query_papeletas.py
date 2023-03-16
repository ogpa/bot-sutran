import json
from graphqlclient import GraphQLClient


#tabla_vehiculos = "Vehiculo-lantl5egqfformu4wl5ale7p6e-dev"
#endpoint = "https://mjga7yrhl5hvlbe5ypz6r27csu.appsync-api.us-east-1.amazonaws.com/graphql"
#api_key = "da2-rcfdc2v4ezezjgdubivb4qwhba"
# Se deben obviar los que tengan _deleted = true


client = GraphQLClient(
    "https://mjga7yrhl5hvlbe5ypz6r27csu.appsync-api.us-east-1.amazonaws.com/graphql")
client.inject_token("da2-rcfdc2v4ezezjgdubivb4qwhba", 'x-api-key')
queryVehiculos = """
  query MyQuery {
  listPapeletas {
    items {
      entidad
      estado_json
    }
  }
}
"""
q = client.execute(queryVehiculos)
print(q)
q = json.loads(q)
print(q)


#query_vehiculos(tabla_vehiculos, endpoint, api_key)
