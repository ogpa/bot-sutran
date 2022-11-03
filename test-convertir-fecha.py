import datetime

xd = "30/06/2022"
a = datetime.datetime.strptime(xd, '%d/%m/%Y').strftime('%Y-%m-%d')
fecha_scan = datetime.datetime.today().strftime("%Y-%m-%d")
print(a)
print(fecha_scan)
