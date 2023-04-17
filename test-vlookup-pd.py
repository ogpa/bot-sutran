import pandas as pd

ruta_cliente_supervisor = "cliente_supervisor.csv"
cliente = "SAN FERNANDO S.A"
df_cliente_supervisor = pd.read_csv(ruta_cliente_supervisor, encoding="ISO-8859-1")
# correo_supervisor = df_cliente_supervisor.query("cliente==" + "'" + cliente + "'")[
#     "correo_supervisor"
# ]
correo_supervisor = df_cliente_supervisor.loc[
    df_cliente_supervisor["cliente"] == cliente, "correo_supervisor"
].item()
print(correo_supervisor)
