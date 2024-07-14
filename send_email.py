import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from configs.configs_email import EMAIL, PASSWORD, SMTP_PORT, SMTP_SERVER


def send_email(recipient_email, subject, body, attachment_file=None):

    msg = MIMEMultipart()
    msg['From'] = EMAIL  
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

   
    if attachment_file:
        with open(attachment_file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attachment_file}"')
            msg.attach(part)

    # Configurações SMTP
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)  
    server.starttls()
    server.login(EMAIL, PASSWORD)  
    server.sendmail(EMAIL, recipient_email, msg.as_string().encode('utf-8'))
    server.quit()

    print("Email sent successfully!")