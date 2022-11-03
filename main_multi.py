from multi_infracciones_sutran_v4 import obtener_datos_papeletas
from multi_verificar_sutran_v2 import verificar_papeletas
from multi_cinemometro_foto_v2 import obtener_fotos
from query_vehiculos import query_vehiculos
from eliminar_repetidas import eliminar_repetidas
from subir_archivos import subir_archivos
from subir_dynamodb import subir_dynamodb


NOMBRE_TABLA_VEHICULOS = "Vehiculo-lantl5egqfformu4wl5ale7p6e-dev"
NOMBRE_TABLA_PAPELETAS = "Papeleta-lantl5egqfformu4wl5ale7p6e-dev"
NOMBRE_BUCKET_S3 = "papeletas-storage-16d23abc230842-dev"
PATH_PUBLIC = "public/"
# Es una lista de placa, id y clienteID
lista_vehiculos_query = query_vehiculos(NOMBRE_TABLA_VEHICULOS)

lista_id_query = []
lista_placa_query = []

for v in lista_vehiculos_query:
    lista_id_query.append(v["id"]["S"])
    lista_placa_query.append(v["placa"]["S"])


# lista_placas_query = ["BKD764", "BLV785", "BDN910", "BEB884", "BEB741", "BHM942", "ATE776", "ATE778", "ATE880", "ATE914", "ATE937" "ATE938", "ATE939", "ATE940", "ATF713", "ATF714",
#                       "ATF715", "ATF716", "ATF720", "ATF730", "ATF747", "ATF748", "ATF749", "ATF752", "ATF761", "ATF762", "ATF763", "ATF765",
#                       "ATF777", "ATF789", "ATF790", "ATF791", "ATF792", "ATF837", "ATF841", "ATF842", "ATF843", "ATF845",
#                       "ATF855", "ATF884", "ATO907", "ATO910", "ATO912", "ATO916", "ATR722", "ATR727", "AUD787", "AVE847"]

dict_datos = obtener_datos_papeletas(lista_placa_query)

dict_papeletas_nuevas = eliminar_repetidas(NOMBRE_TABLA_PAPELETAS, dict_datos)

if (len(dict_papeletas_nuevas["numdocumento"]) > 0):

    dict_verificar = verificar_papeletas(dict_papeletas_nuevas)
    del dict_verificar["numdocumento"]

    dict_verificar_nuevas = dict_papeletas_nuevas | dict_verificar

    dict_fotos = obtener_fotos(dict_verificar_nuevas,
                               NOMBRE_BUCKET_S3, PATH_PUBLIC)
    del dict_fotos["numdocumento"]

    papeletas_dict = dict_verificar_nuevas | dict_fotos

    subir_dynamodb(NOMBRE_TABLA_PAPELETAS, papeletas_dict,
                   lista_id_query, lista_placa_query)
    subir_archivos(NOMBRE_BUCKET_S3, PATH_PUBLIC, papeletas_dict)

else:
    print("No hay papeletas nuevas!")
