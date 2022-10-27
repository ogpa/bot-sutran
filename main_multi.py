from multi_infracciones_sutran_v4_sema import obtener_datos_papeletas
#from multi_verificar_sutran import verificar_papeletas
#from multi_cinemometro_foto_v2 import obtener_fotos
import pandas as pd
# 48 placas
lista_placas = ["BLV785", "BKD764", "BDN910", "BEB884", "BEB741", "BHM942", "ATE776", "ATE778", "ATE880", "ATE914", "ATE937" "ATE938", "ATE939", "ATE940", "ATF713", "ATF714",
                "ATF715", "ATF716", "ATF720", "ATF730", "ATF747", "ATF748", "ATF749", "ATF752", "ATF761", "ATF762", "ATF763", "ATF765",
                "ATF777", "ATF789", "ATF790", "ATF791", "ATF792", "ATF837", "ATF841", "ATF842", "ATF843", "ATF845",
                "ATF855", "ATF884", "ATO907", "ATO910", "ATO912", "ATO916", "ATR722", "ATR727", "AUD787", "AVE847"]

# Aquí se debe obtener la lista de placas de la BD. También el cliente, supervisor y correo de supervisor

dict_datos = obtener_datos_papeletas(lista_placas)

# Aquí se debe verificar si las papeletas se repiten con lo que ya se encuentra en la BD


# dict_verificar = verificar_papeletas(dict_datos)
# dict_fotos = obtener_fotos(dict_datos)

# # print(dict_datos)
# del dict_verificar["numdocumento"]
# del dict_fotos["numdocumento"]
# # print(dict_verificar)
# # print(dict_fotos)

# papeletas_dict = dict_datos | dict_verificar | dict_fotos

# print(papeletas_dict)
# papeletas_df = pd.DataFrame(papeletas_dict)

# csv_filename = "papeletas.csv"

# papeletas_df.to_csv(csv_filename, index=False)
