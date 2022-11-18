import boto3
from botocore.exceptions import ClientError
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

AWS_REGION = "us-east-1"

message = MIMEMultipart()
message['From'] = "Diego Prueba <innovacion@mb-renting.com>"
destinatarios = ['diego_1021_@outlook.com', 'diego.pizarro@pucp.pe']
destinatarios.append("dpizarro@mb-renting.com")
message['Subject'] = "Prueba append"
message['To'] = ", ".join(destinatarios)
part = MIMEText('Hola!!!!11111!!1!', 'html')
message.attach(part)


# attachment

part = MIMEApplication(
    open("BKD764_2022-06-30_2450293528.jpg", 'rb').read())
part.add_header('Content-Disposition', 'attachment',
                filename='BKD764_2022-06-30_2450293528.jpg')
message.attach(part)

BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
             )
BODY_HTML = """
<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
"""

CHARSET = "UTF-8"

client = boto3.client('ses', region_name=AWS_REGION)

try:
    # Provide the contents of the email.
    response = client.send_raw_email(
        Source=message['From'],
        Destinations=destinatarios,
        RawMessage={
            'Data': message.as_string()
        },
        # If you are not using a configuration set, comment or delete the
        # following line
        # ConfigurationSetName=CONFIGURATION_SET,
    )
# Display an error if something goes wrong.
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])
