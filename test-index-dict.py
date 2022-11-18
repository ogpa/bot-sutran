lista = [{'correo_supervisor': 'ecarrascal@mb-renting.com', 'correo_comercial': 'rguerrero@mb-renting.com', 'placa': 'San Fernando'},
         {'correo_supervisor': 'diego.pizarro@pucp.pe', 'correo_comercial': 'diego_1021_@outlook.com', 'placa': 'Avgust'}]
placa = 'San Fernando'
for v in lista:
    print(v["placa"])
    if v["placa"] == placa:
        # Es el index de todo el conjunto de datos, no de solo la placa
        print(v["correo_supervisor"])
        # print("xd")
