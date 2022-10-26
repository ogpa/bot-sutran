from function_infracciones_sutran import obtener_datos_papeletas
from function_verificar_sutran import obtener_datos_adicionales

# Se obtiene dictionary
lista_placas = ["BLV785", "AVE847", "BDN910"]

dict_datos = obtener_datos_papeletas(lista_placas)

dict_verificar = obtener_datos_adicionales(dict_datos)

# print(dict_datos)
# print(dict_verificar)

dict_final = dict_datos | dict_verificar
print(dict_final)
