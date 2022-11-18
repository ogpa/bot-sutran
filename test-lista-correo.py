listacorreo = [[{'cliente': 'Avgust'}, {'correos': ['diego.pizarro@pucp.pe', 'diego_1021_@outlook.com']}, {'tablahtml': [['BDN910', '21/10/2020', '828', '878.60', '2450068335', 'SUTRAN']]}, {'path': ['BDN910_2020-10-21_2450068335.jpg']}],
               [{'cliente': 'San Fernando'}, {'correos': ['ecarrascal@mb-renting.com', 'rguerrero@mb-renting.com']}, {'tablahtml': [['BKD764', '30/06/2022', '828', '828', '2450293528', 'SUTRAN']]}, {'path': ['BKD764_2022-06-30_2450293528.jpg']}]]

for x in listacorreo:
    print(x[2]["tablahtml"])
