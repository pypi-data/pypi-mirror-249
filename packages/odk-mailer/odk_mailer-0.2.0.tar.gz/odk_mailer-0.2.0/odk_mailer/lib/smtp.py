from odk_mailer.lib import globals, utils
from email.message import EmailMessage
import smtplib

def send_mail(subject, sender, recipient, message, type='plain'):

    config = globals.odk_mailer_config

    if not config:
        utils.abort("Config error.")

    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = sender
    email['To'] = recipient
    email.set_content(message, subtype=type)

    try:
        smtp = smtplib.SMTP(timeout=5)
        smtp.set_debuglevel(2)
        smtp.connect(config.smtp_host, config.smtp_port)
        smtp.send_message(email)
        smtp.quit()
        print("Successfully sent email to " + email["To"])
    except Exception as error:
        print(error)