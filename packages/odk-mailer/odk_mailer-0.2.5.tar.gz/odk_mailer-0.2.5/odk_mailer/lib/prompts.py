import inquirer
from odk_mailer.lib import validators

def source():
    questions = [
        inquirer.List('type', 
                    message="Select source type:",
                    choices= [
                        ("CSV file.", "file"),
                        ("ODK API", "api")
                    ],                      
                    carousel=True
        ),
        inquirer.Path('file_path',
                    message="Input local path to CSV file",
                    path_type=inquirer.Path.FILE,
                    exists=True,
                    normalize_to_absolute_path=True,
                    ignore=lambda x: x["type"] == "api"
        ),
        inquirer.Text('api_form',
                    message="Input form/attachment name",                      
                    ignore=lambda x: x["type"] == "file"
                    #tbd: add regex valdation
        ),
        inquirer.Text('api_proj',
                    message="Input project id",
                    validate= validators.int_only,
                    ignore=lambda x: x["type"] == "file"
        ),
        inquirer.Text('api_host',
                    message="Input ODK host url",
                    ignore=lambda x: x["type"] == "file",
                    # tbd validate url, https
        ),
        inquirer.Text('api_user',
                    message="Input ODK username",
                    ignore=lambda x: x["type"] == "file"
        ),
        inquirer.Password('api_pass',
                    message="Input ODK password",
                    ignore=lambda x: x["type"] == "file"
        )
    ]
    return inquirer.prompt(questions, raise_keyboard_interrupt=True)

def fields(headers=[]):
    questions = [
        inquirer.List('email',
                    message="Select email field",
                    choices=headers,
                    default='email' if 'email' in headers else "",
                    carousel=True
        ),
        inquirer.Checkbox("data", 
                    message="Select data field(s)",
                    choices= lambda x: filter(lambda y: y != x["email"], headers)
        )        
    ]
    return inquirer.prompt(questions, raise_keyboard_interrupt=True)

def message():
    questions = [
        inquirer.Text('sender',
                    message="Input message sender",
                    default="odk@swisstph.ch",  # remove
                    validate=validators.email_address                      
        ),
        inquirer.List('format', 
                    message="Select message format:",
                    choices= [
                        ("Text", "txt"),
                         ("HTML", "html")
                    ],                      
                    carousel=True
        ),
        inquirer.List('source', 
                    message="Select message source:",
                    choices= [
                        ("Input as string", "stdin"),
                        ("File from path", "path")
                    ],                      
                    carousel=True
        ),        
        inquirer.Text('content_stdin',
                    message="Input message string",
                    ignore=lambda x: x["source"] != "stdin",
                    validate= validators.not_empty
        ),
        inquirer.Path('content_path',
                    message="Message file path",
                    path_type=inquirer.Path.FILE,
                    exists=True,
                    normalize_to_absolute_path=True,
                    ignore=lambda x: x["source"] != "path"
                    
        )
    ]
    return inquirer.prompt(questions, raise_keyboard_interrupt=True)

def schedule():
    questions = [
        inquirer.List('now',
                    message="Send immediately now or schedule for later?",
                    choices=[
                        ("Send now",True),
                        ("Schedule for later", False)
                    ]
        ),
        inquirer.Text('future',
                    message="Input schedule time and date",
                    ignore=lambda x: x["now"] == True,
                    validate= validators.date_format
        )
    ]

    return inquirer.prompt(questions, raise_keyboard_interrupt=True)

def confirm():
    return inquirer.prompt(
        [
            inquirer.Confirm("confirm", message="Create MailJob?")
        ], 
        raise_keyboard_interrupt=True)