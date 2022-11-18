import boto3
import json
from graphqlclient import GraphQLClient


#tabla_papeletas = "Papeleta-lantl5egqfformu4wl5ale7p6e-dev"

# Se deben obviar los que tengan _deleted = true


def query_papeletas(tabla_papeletas, endpoint, api_key):
    client = GraphQLClient(endpoint)
    client.inject_token(api_key, 'x-api-key')
    queryPapeletas = """
  query MyQuery {
  listPapeletas {
    items {
      id
      num_documento
    }
  }
}
"""
    q = client.execute(queryPapeletas)
    q = json.loads(q)
    # print(q)
    return q


#query_papeletas(tabla_papeletas, endpoint, api_key)
