import pandas as pd

ruta_placas_cliente = "placas_cliente_detalles.csv"
ruta_cliente_supervisor = "cliente_supervisor.csv"
# df = pd.read_csv(ruta_placas_cliente, encoding="ISO-8859-1")

# # 36 elementos

# df = df[df["cliente"].str.contains("Vendida|vendida|VENDIDA") == False]
df = pd.read_csv(ruta_cliente_supervisor, encoding="ISO-8859-1")
df.fillna("", inplace=True)
print(df)
