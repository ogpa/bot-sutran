import boto3

client = boto3.client("dynamodb")

tabla_papeletas = "Papeleta-lantl5egqfformu4wl5ale7p6e-dev"

# Se deben obviar los que tengan _deleted = true


def query_papeletas(tabla_papeletas):
    response_vehiculos = client.scan(
        TableName=tabla_papeletas,
        ProjectionExpression='#i,#p,#d,#n',
        ExpressionAttributeNames={
            "#i": "id",
            "#p": "placa",
            "#d": "_deleted",
            "#n": "num_documento"
        },
        FilterExpression='#d <> :d',
        ExpressionAttributeValues={":d": {"BOOL": True}}

    )
    print(response_vehiculos["Items"])
    # return (response_vehiculos["Items"])


query_papeletas(tabla_papeletas)
