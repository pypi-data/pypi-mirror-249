import typer
import csv
from email_validator import validate_email, EmailNotValidError

# return unformatted string instead of raising error
# when key is missing within dictionary
# https://stackoverflow.com/a/17215533/3127170
class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

class Recipients:
    def __init__(self, path):
        self.path  = path
        self.fieldnames = []
        self.data = []

        self.isValid = False
        self.invalidEmails = []

        # Initialize 
        self.init()

    def init(self):

        # # invalid file extension
        # ext = os.path.splitext(self.path)[-1].lower()
        # if not ext == ".csv":
        #     raise typer.Exit("Invalid file extension.")

        # # invalid file path
        # if not os.path.isfile(self.path):
        #     raise typer.Exit("Invalid file path.")

        # read data
        with open(self.path, newline='') as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            self.fieldnames = reader.fieldnames
            for row in reader:
                self.data.append(row)

    def validate(self, email_field):
        invalid_emails = []
        total = 0

        print("\nValidating recipients...")
        with typer.progressbar(self.data) as progress:
            for row in progress:
                total += 1
                email = row[email_field]
                try:
                    if not email:
                        raise EmailNotValidError("Email address missing. Check for missing delimiters (',') in your CSV file.")
                    # Disable DNS checks since this can be blocked for unknown reasons within network.
                    validate_email(email, check_deliverability=True)
                except EmailNotValidError as e:
                    invalid = [str(total) ,email, str(e)]
                    invalid_emails.append(invalid)
                
        print(f"Validated {total} entries.\n")

        self.invalidEmails = invalid_emails
        self.numEmails = len(self.data)
        
        if len(invalid_emails) == 0:
            self.isValid = True

        return self.isValid

    # def test_filling(self):
    #     print(self.fieldnames)
    #     print(f'file path is {self.path}')
        
    #     txt = "The firstname is {firstname}\n lastname is {lastname} \n email is {email} \n not filled {not_filled}"
    #     for row in self.data:
    #         print(txt.format_map(SafeDict(row)))