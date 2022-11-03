import boto3
from multiprocessing.pool import ThreadPool

s3 = boto3.client('s3')


def subir_archivos(bucket, path_public, papeletas_dict):
    lista_de_archivos = papeletas_dict["path"]

    def subir(archivo):
        with open(archivo, "rb") as f:
            s3.upload_fileobj(f, bucket, path_public + archivo)

    pool = ThreadPool(processes=len(lista_de_archivos)*2)
    pool.map(subir, lista_de_archivos)
    print("Se subieron todos los archivos a S3.")
