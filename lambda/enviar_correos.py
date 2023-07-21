import boto3
from botocore.exceptions import ClientError
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from datetime import date
from tabulate import tabulate
import numpy as np

CORREOS_EXTRA = ["dpizarro@mb-renting.com"]
today = date.today()
hoy = today.strftime("%d/%m/%Y")
AWS_REGION = "us-east-1"
CABECERAS_TABLA = [
    "Placa",
    "Fecha",
    "Tipo documento",
    "Monto",
    "Monto pronto pago",
    "Número de papeleta",
    "Entidad",
]


def crear_body(tablahtml):
    tabla_html = tabulate(tablahtml, tablefmt="html", headers=CABECERAS_TABLA)
    body = (
        """
<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

</style>
</head>
<body>
  <h1>Nuevas papeletas al """
        + hoy
        + """</h1>
  <p>Lista de nuevas papeletas. Puede verificarlas en el siguiente enlace: <a target=_blank href=http://www.sutran.gob.pe/consultas/record-de-infracciones/verifica-tu-infraccion/>Verifica tu infracción SUTRAN.</a></p>
      """
        + tabla_html
        + """
  <p>En caso MB Renting realice el pago a nombre del cliente, el monto total tendrá un cargo del 10% por gastos administrativos.</p>
</body>
</html>
"""
    )
    return body


client = boto3.client("ses", region_name=AWS_REGION)


def enviar_correos(lista_para_enviar_correos):
    for x in lista_para_enviar_correos:
        body = crear_body(x[2]["tablahtml"])
        message = MIMEMultipart()
        part = MIMEText(body, "html")
        message.attach(part)
        correos_destinarios_incluido_diego = x[1]["correos"]
        if (
            correos_destinarios_incluido_diego == None
            or correos_destinarios_incluido_diego == ""
            or correos_destinarios_incluido_diego == [""]
        ):
            correos_destinarios_incluido_diego = []
        for c in CORREOS_EXTRA:
            correos_destinarios_incluido_diego.append(c)
        print(correos_destinarios_incluido_diego)
        message["From"] = "Papeletas <innovacion@mb-renting.com>"
        message["Subject"] = "Papeletas " + x[0]["cliente"]
        message["To"] = ", ".join(correos_destinarios_incluido_diego)
        # Adjuntar imágenes
        print(x[3]["path"])
        for p in x[3]["path"]:
            try:
                part = MIMEApplication(open(p, "rb").read())
                part.add_header("Content-Disposition", "attachment", filename=p)
                message.attach(part)
            except:
                continue

        filename = x[0]["cliente"] + ".html"

        with open(filename, "w") as file:
            file.write(body)
        try:
            # Provide the contents of the email.
            response = client.send_raw_email(
                Source=message["From"],
                Destinations=correos_destinarios_incluido_diego,
                RawMessage={"Data": message.as_string()},
            )

        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print("Correo enviado! ID del correo:"),
            print(response["MessageId"])


# tabla = [['one', 'two', 'three', 'four'], [
#     'five', 'six', 'seven', 'eight'], ['9', '10', '11', '12']]


# CHARSET = "UTF-8"
# attachment
# filename = "ejem.html"
# with open(filename, 'w') as file:
#     file.write(body)
