import boto3
from multiprocessing.pool import ThreadPool

s3 = boto3.client('s3')

# Se crea una carpeta por placa y subfolder "Papeletas"
# Ejemplo: public/ABC123/Papeletas/245012/245012.jpg


def subir_archivos(bucket, path_public, papeletas_dict):
    lista_de_archivos = papeletas_dict["path"]
    lista_de_placas = papeletas_dict["placa"]
    lista_de_numdocumentos = papeletas_dict["numdocumento"]
    cantidad_archivos = len(lista_de_archivos)

    for x in range(cantidad_archivos):
        with open(lista_de_archivos[x], "rb") as f:
            s3.upload_fileobj(
                f, bucket, path_public + lista_de_placas[x] + "/" + "Papeletas/" + lista_de_numdocumentos[x] + "/" + "Papeleta_" + lista_de_archivos[x])
            # Ejemplo: public/ABC123/Papeletas/245012/Papeleta_245012.jpg

    # def subir(archivo):
    #     with open(archivo, "rb") as f:
    #         s3.upload_fileobj(f, bucket, path_public + archivo)

    # pool = ThreadPool(processes=len(lista_de_archivos)*2)
    # pool.map(subir, lista_de_archivos)
    print("Se subieron todos los archivos a S3.")
