from multi_infracciones_sutran_v3 import obtener_datos_papeletas
from multi_verificar_sutran import verificar_papeletas
from multi_cinemometro_foto_v2 import obtener_fotos
import numpy as np

lista_placas = ["BLV785", "BKD764", "BDN910", "BEB884", "BEB741", "BHM942", "ATE776", "ATE778", "ATE880", "ATE914", "ATE937" "ATE938", "ATE939", "ATE940", "ATF713", "ATF714",
                "ATF715", "ATF716", "ATF720", "ATF730", "ATF747", "ATF748", "ATF749", "ATF752", "ATF761", "ATF762", "ATF763", "ATF765",
                "ATF777", "ATF789", "ATF790", "ATF791", "ATF792", "ATF837", "ATF841", "ATF842", "ATF843", "ATF845",
                "ATF855", "ATF884", "ATO907", "ATO910", "ATO912", "ATO916", "ATR722", "ATR727", "AUD787"]

dict_datos = obtener_datos_papeletas(lista_placas)
dict_verificar = verificar_papeletas(dict_datos)
dict_fotos = obtener_fotos(dict_datos)

print(dict_datos)
print(dict_verificar)
print(dict_fotos)

# Ordenar los 3 en base a la lista numdocumento. Luego unir los 3 y eliminar las 2 listas numdocumentos sobrantes
