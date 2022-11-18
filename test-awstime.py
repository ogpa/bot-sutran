from datetime import datetime

hora = datetime.now().time()
hora = str(hora)
hora = hora[:-3]
print(hora)
