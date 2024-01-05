from odk_mailer.lib import db, smtp
# from email.message import EmailMessage
# from smtplib import SMTP
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

    def __init__(self, id: str):
        self.hash = id
        
        job = db.getJob(self.hash)
        message = job["message"]
        # get all relevant stuff here
        self.subject = "ODK-MAILER: New Mail Job" + self.hash
        self.sender = message["sender"]
        self.recipients = job["recipients"]
        self.content = message["content"]

    def send(self, dry=False):

        print(self.hash)
        print("================================================================")
        print("Sending emails..")    


        # Prepare SMTP
        smtp_host = 'smtp.freesmtpservers.com'
        smtp_port = 25
        smtp_username = ''
        smtp_password = ''

        # Set SMTP 
        # https://docs.python.org/3/library/smtplib.html#smtplib.SMTP_SSL
        # https://docs.python.org/3/library/email.examples.html#email-examples
        # required smtp parameters
        #smtp_host = os.getenv('SMTP_HOST')
        #smtp_port = os.getenv('SMTP_PORT')
        #smtp_username = os.getenv('SMTP_USERNAME')
        #smtp_password = os.getenv('SMTP_PASSWORD')

        for recipient in self.recipients:

            # Prepare Message
            text = self.content
            
            message = text.format_map(SafeDict(recipient))

            smtp.send_mail(self.subject,self.sender, recipient["email"], message)

            # Prepare Email
            # https://stackoverflow.com/a/58318206/3127170
            # from email.message import EmailMessage
            # from smtplib import SMTP
            # construct email
            # email = EmailMessage()
            # email['Subject'] = self.subject
            # email['From'] = self.sender
            # email['To'] = recipient["email"]
            # email.set_content(message, subtype='plain')


            # # Send the message via local SMTP server.
            # with SMTP(smtp_host, smtp_port) as s:
            #     #s.login('foo_user', 'bar_password')
            #     s.send_message(email)
            #     print(f"Sending mail to {recipient['email']}")

