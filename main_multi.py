from multi_infracciones_sutran_v3 import obtener_datos_papeletas
from multi_verificar_sutran import verificar_papeletas
from multi_cinemometro_foto_v2 import obtener_fotos

lista_placas = ["BLV785", "BKD764","AVE847", "BDN910"]

dict_datos = obtener_datos_papeletas(lista_placas)
dict_verificar = verificar_papeletas(dict_datos)
dict_fotos = obtener_fotos(dict_datos)

print(dict_datos)
print(dict_verificar)
print(dict_fotos)