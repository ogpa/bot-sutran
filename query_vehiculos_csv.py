import boto3
from unir_placas_clientes_supervisores_csv import unir_placas_clientes_supervisores_csv

s3 = boto3.client("s3")


def query_vehiculos_csv():
    OBJECT_S3_PLACAS = "bi-telemetria/datasets/placas_cliente_detalles.csv"
    BUCKET_S3_PLACAS = "apps-mbr-innovacion"
    ruta_lambda_placas = "placas_cliente_detalles.csv"

    with open(ruta_lambda_placas, "wb") as f:
        s3.download_fileobj(BUCKET_S3_PLACAS, OBJECT_S3_PLACAS, f)

    OBJECT_S3_SUPERVISORES = "bi-telemetria/datasets/cliente_supervisor.csv"
    BUCKET_S3_SUPERVISORES = "apps-mbr-innovacion"
    ruta_lambda_supervisores = "cliente_supervisor.csv"

    with open(ruta_lambda_supervisores, "wb") as f:
        s3.download_fileobj(BUCKET_S3_SUPERVISORES, OBJECT_S3_SUPERVISORES, f)

    df_placas_clientes_supervisores = unir_placas_clientes_supervisores_csv(
        ruta_lambda_placas, ruta_lambda_supervisores
    )

    return df_placas_clientes_supervisores


# query_vehiculos_csv()
