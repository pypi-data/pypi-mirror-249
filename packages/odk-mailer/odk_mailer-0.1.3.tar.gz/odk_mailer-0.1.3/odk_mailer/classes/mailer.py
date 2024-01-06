from odk_mailer.lib import db, globals
from email.message import EmailMessage
import smtplib
import os

# return unformatted string instead of raising error
# when key is missing within dictionary
# https://stackoverflow.com/a/17215533/3127170
class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}' 
    

class Mailer:
    hash: str
    sender:str
    format: str
    content: str
    recipients: []

    subject: str
    body: str
    sender: str
    headers: str

    def __init__(self, id: str, verbose:bool):
        self.hash = id
        self.verbose = verbose
        job = db.getJob(self.hash)

        self.subject = "ODK-MAILER: New Mail Job" + self.hash # tbd: add text prompt, add to self.message
        self.message = job.message
        self.recipients = job.recipients

    def send(self, dry=False):

        print(self.hash)
        print("================================================================")
        print("Sending emails..")

        idx=0
        for recipient in self.recipients:

            print()
            print(f"(#{idx+1}) Attempting to send.. ")
            text = self.message.content
            # Prepare Message           
            success = self.smtp(
                recipient.email, 
                text.format_map(SafeDict(vars(recipient)))
            )

            idx = idx + 1


    def smtp(self, recipient, message, type='plain'):

        email = EmailMessage()
        email['Subject'] = self.subject
        email['From'] = self.message.sender
        email['To'] = recipient
        email.set_content(message, subtype=type)

        try:
            smtp = smtplib.SMTP(timeout=5)
            if self.verbose:
            # enable debugging by CLI flag --debug
                smtp.set_debuglevel(2)
            smtp.connect(globals.odk_mailer_config.smtp_host, globals.odk_mailer_config.smtp_port)

            if hasattr(globals.odk_mailer_config, 'smtp_user') and hasattr(globals.odk_mailer_config, 'smtp_pass'):
                smtp.login(globals.odk_mailer_config.smtp_user, globals.odk_mailer_config.smtp_pass)
            # if username and password are supplied, perform smtp.login()
            # requires additional actions, such as setting TLS or SSL
            smtp.send_message(email)
            smtp.quit()
            # write into /log/timestamp_<hash>.log
            # log.write("Successfully sent email to " + email["To"])
            return True
        except Exception as error:
            # write into /log/timestamp_<hash>.log
            # raise exception to interrupt loop
            print(error)
            print("Failed sending mail to: " + email['To'])
            print()
            return False