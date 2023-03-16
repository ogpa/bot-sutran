
def agregar_correos_dict(papeletas, cliente, lista_correos):
    index_repetidos = (i for i, value in enumerate(
        papeletas["cliente"]) if value == cliente)
    # for p in papeletas["cliente"]:

    #     if p == cliente:
    #         idx = papeletas["cliente"].index(p)
    #         print(idx)
    #         papeletas["destinatarios_correoenviado"][idx] = lista_correos

    for r in index_repetidos:
        papeletas["destinatarios_correoenviado"][r] = lista_correos
    return papeletas
