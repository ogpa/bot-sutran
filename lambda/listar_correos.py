import numpy as np
import datetime
from obtener_correos import obtener_correos
from agregar_correos_dict import agregar_correos_dict


def unicos(lista):
    x = np.array(lista)
    return np.unique(x)


def listar_correos(papeletas, ruta_cliente_supervisor):
    # papeletas = {'placa': ['BKD764', 'BKD764'], 'numdocumento': ['2450293528', '2450291852'], 'tipodocumento': ['Papeletas Transito', 'Papeletas Transito'], 'fechadocumento': ['2022-06-30', '2022-06-23'], 'codigoinfraccion': ['M20', 'M20'], 'clasificacion': ['Muy Grave', 'Muy Grave'], 'entidad': ['SUTRAN', 'SUTRAN'], 'fechascan': ['2023-04-16', '2023-04-16', '2023-04-16', '2023-04-16'], 'agenteinfractor': ['Propietario', 'Propietario'], 'nombreinfractor': ['MB RENTING SA', 'MB RENTING SA'], 'montoinfraccion': ['891', '1188'], 'montoprontopago': ['891', '1188'], 'estado': ['PENDIETE DE PAGO', 'PENDIETE DE PAGO'], 'cliente': ['SAN FERNANDO', 'SAN FERNANDO'], 'path': ['BKD764_2022-Junio-30_2450293528.jpg', 'BKD764_2022-Junio-23_2450291852.jpg'], 'extension': ['jpg', 'jpg']}

    # Esto es para añadir de antemano la lista de destinatarios
    longitud_papeletas = len(papeletas["cliente"])

    ###########################################################
    lista_clientes = papeletas["cliente"]
    clientes_unicos = unicos(lista_clientes)
    lista_clientes_unicos = clientes_unicos.tolist()
    # longitud_listacorreos = len(lista_clientes_unicos)
    lista_destinatarios_correoenviado = [None] * longitud_papeletas
    papeletas["destinatarios_correoenviado"] = lista_destinatarios_correoenviado
    # print(lista_clientes_unicos)

    # lista_total = [None]*longitud_listacorreos

    # keys del dictionario
    # tablahtml :
    # cliente :
    # listacorreos : correos del supervisor y comercial
    # Doble lista: lista [lista, lista, lista]
    # tabla = [['one', 'two', 'three', 'four'], [
    # 'five', 'six', 'seven', 'eight'], ['9', '10', '11', '12']]
    #
    #
    # lista_correos = obtener_correos(clientes_unicos,endpoint,api_key)
    lista_total = []
    for c_u in lista_clientes_unicos:
        lista_temp_html = []
        lista_temp_path = []
        x = range(len(lista_clientes))
        for c_l in x:
            if lista_clientes[c_l] == c_u:
                # if c_l == c_u:

                # id_c_u = lista_clientes_unicos.index(c_u)
                # id_c_l = lista_clientes.index(c_l)
                # Esto es para el key tabla html
                # fecha_documento = datetime.datetime.strptime(
                #     papeletas["fechadocumento"][id_c_l], "%Y-%m-%d").strftime("%d/%m/%Y")
                # lista_temp_html.append([papeletas["placa"][id_c_l], fecha_documento, papeletas["montoinfraccion"]
                #                        [id_c_l], papeletas["montoprontopago"][id_c_l], papeletas["numdocumento"][id_c_l], papeletas["entidad"][id_c_l]])
                # lista_temp_path.append(papeletas["path"][id_c_l])
                fecha_documento = datetime.datetime.strptime(
                    papeletas["fechadocumento"][c_l], "%Y-%m-%d"
                ).strftime("%d/%m/%Y")
                lista_temp_html.append(
                    [
                        papeletas["placa"][c_l],
                        fecha_documento,
                        papeletas["tipodocumento"][c_l],
                        papeletas["montoinfraccion"][c_l],
                        papeletas["montoprontopago"][c_l],
                        papeletas["numdocumento"][c_l],
                        papeletas["entidad"][c_l],
                    ]
                )
                lista_temp_path.append(papeletas["path"][c_l])

        d_path = {"path": lista_temp_path}
        # Termina de scanear todos los datos que coinciden con un cliente y guardo todo eso en el diccionario total
        d_tablahtml = {"tablahtml": lista_temp_html}
        # Aquí tengo que hacer append de lo que solo coloco una vez por cliente como correo supervisor, etc
        d_cliente = {"cliente": c_u}
        # En d_correos debe haber una lista con los correos de supervisor y comercial
        # Esta lista la saco con un query de clientes
        # lista_correos = obtener_correos(c_u, endpoint, api_key)
        lista_correos = obtener_correos(c_u, ruta_cliente_supervisor)
        print("lista_correos")
        print(lista_correos)
        papeletas_con_correo = agregar_correos_dict(papeletas, c_u, lista_correos)
        d_correos = {"correos": lista_correos}
        lista_total.append([d_cliente, d_correos, d_tablahtml, d_path])

    print(papeletas_con_correo)
    print(lista_total)
    return lista_total, papeletas_con_correo
