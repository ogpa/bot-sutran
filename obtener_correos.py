import pandas as pd

# GRAPHQL_ENDPOINT = 'https://mjga7yrhl5hvlbe5ypz6r27csu.appsync-api.us-east-1.amazonaws.com/graphql'
# API_KEY = "da2-rcfdc2v4ezezjgdubivb4qwhba"


# def obtener_correos(cliente, endpoint, api_key):
def obtener_correos(cliente, ruta_cliente_supervisor):
    # client = GraphQLClient(endpoint)
    # client.inject_token(api_key, "x-api-key")
    # lista_clientes = ["San Fernando", "Avgust"]
    # input_clientes = ''
    # for c in lista_clientes:
    #     input_clientes = input_clientes + '{ nombre: { eq: "' + c + '" } },'
    # input_clientes = input_clientes[:-1]
    #     queryClientes = (
    #         """
    #   query MyQuery {
    #   listClientes(filter: {
    #     or: [
    #     { nombre: { eq: """
    #         + '"'
    #         + cliente
    #         + '"'
    #         + """ } }
    #     ],
    #     and:[
    #        { v_supervisor: { eq: "v0_supervisor" } }
    #     ]
    #   }) {
    #     items {
    #       correo_supervisor
    #       correo_comercial
    #       nombre
    #     }
    #   }
    # }
    # """
    #     )
    #     q = client.execute(queryClientes)
    #     q = json.loads(q)
    # print(q["data"]["listClientes"]["items"])
    print(cliente)
    # print(df_placas_clientes_supervisores)
    df_cliente_supervisor = pd.read_csv(ruta_cliente_supervisor, encoding="ISO-8859-1")
    # Bureau Veritas
    # q = q["data"]["listClientes"]["items"]
    # print(q)
    # cant_placas = len(df_placas_clientes_supervisores.index)
    # correo_supervisor = df_placas_clientes_supervisores["correo_supervisor"].where(
    #     df_placas_clientes_supervisores["cliente"] == cliente
    # )
    # print("cliente==" + "'" + cliente + "'")
    correo_supervisor = df_cliente_supervisor.loc[
        df_cliente_supervisor["cliente"] == cliente, "correo_supervisor"
    ].item()
    print(correo_supervisor)
    # [{'correo_supervisor': 'dpizarro@mb-renting.com', 'correo_comercial': 'dpizarro@mb-renting.com', 'nombre': 'Bureau Veritas'}]
    # lista_correos = [q[0]["correo_supervisor"], q[0]["correo_comercial"]]
    lista_correos = [correo_supervisor]
    return lista_correos


# obtener_correos(lista_clientes,GRAPHQL_ENDPOINT,API_KEY)
