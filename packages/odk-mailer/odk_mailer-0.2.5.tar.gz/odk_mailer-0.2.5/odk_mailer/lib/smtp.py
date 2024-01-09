from odk_mailer.lib import globals, utils
from email.message import EmailMessage
import smtplib

def send_mail(sender, recipient, host, port):

    subject = "Test Mail"
    message = "This is a test mail."

    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = sender
    email['To'] = recipient
    email.set_content(message, subtype="plain")

    try:
        smtp = smtplib.SMTP(timeout=5)
        smtp.set_debuglevel(2)
        smtp.connect(host, port)
        smtp.send_message(email)
        smtp.quit()
        print("Successfully sent email to " + email["To"])
    except Exception as error:
        print(error)
