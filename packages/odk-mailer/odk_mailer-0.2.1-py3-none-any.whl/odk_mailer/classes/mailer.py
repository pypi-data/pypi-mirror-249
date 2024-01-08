import os
from types import SimpleNamespace
import smtplib
from email.message import EmailMessage
from odk_mailer.lib import globals, utils
import json

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

    def __init__(self, hash: str, dry: bool, verbose:bool, config):
        self.hash = hash
        self.verbose = verbose
        self.config = config
        self.dry = dry

        with open(os.path.join(globals.odk_mailer_job, self.hash+'.json'), 'r', encoding='utf-8') as f:
            job = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        self.subject = "ODK-MAILER: New Mail Job" + self.hash # tbd: add text prompt, add to self.message
        self.message = job.message
        self.recipients = job.recipients

    def send(self):

        # print(self.hash)
        # print("================================================================")
        # print("Sending emails..")

        idx=0
        for recipient in self.recipients:

            text = self.message.content
            # Prepare Message
            if self.dry: 
                print(f"#{idx}")
                print(recipient.email)
                print(text.format_map(SafeDict(vars(recipient))))
            else: 
                print()
                print(f"(#{idx+1}) Attempting to send.. ")
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
            smtp.connect(self.config.smtp_host, self.config.smtp_port)

            if hasattr(self.config, 'smtp_user') and hasattr(self.config, 'smtp_pass'):
                smtp.login(self.config.smtp_user, self.config.smtp_pass)
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