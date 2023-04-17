import pandas as pd


ruta_placas_cliente = "placas_cliente_detalles.csv"
ruta_cliente_supervisor = "cliente_supervisor.csv"


def eliminar_guion(placa):
    placa_sin_guion = placa.replace("-", "")
    return placa_sin_guion


lista_placas_cliente = []


def unir_placas_clientes_supervisores_csv(ruta_placas_cliente, ruta_cliente_supervisor):
    df_placas_cliente = pd.read_csv(ruta_placas_cliente, encoding="ISO-8859-1")
    # df_cliente_supervisor = pd.read_csv(ruta_cliente_supervisor, encoding="ISO-8859-1")
    # df_total = df_placas_cliente.merge(df_cliente_supervisor, how="left", on="cliente")

    # Eliminar guiones
    df_placas_cliente["placa"] = df_placas_cliente["placa"].apply(eliminar_guion)
    # df_total["placa"] = df_total.apply(lambda x: eliminar_guion(x["placa"]), axis=1) #Es lo mismo de arriba

    # df_total.to_csv("total_placa_cliente_supervisor.csv", index=False)
    # print(df_total)
    cant_placas = len(df_placas_cliente.index)
    # print(len(df_total.index))
    # for x in range(6):
    for x in range(cant_placas):
        lista_placas_cliente.append(
            {
                "placa": df_placas_cliente["placa"][x],
                "cliente": df_placas_cliente["cliente"][x],
            }
        )
    print(lista_placas_cliente)
    return lista_placas_cliente


# unir_placas_clientes_supervisores_csv(ruta_placas_cliente, ruta_cliente_supervisor)
