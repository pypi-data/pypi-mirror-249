from inquirer import errors
from odk_mailer.lib import utils
from odk_mailer.classes.job import Source, Fields, Message, Schedule
import re
import os
from datetime import datetime
import time

def source(s_str: str):

    s_lst = s_str.split("::", 6)
    s_len = len(s_lst)

    if not s_len in [2,6]:        
        utils.abort("Invalid file/api source string")

    if s_len == 2:
        s_type = s_lst[0]
        s_path = s_lst[1]

        if s_type != "file":
            utils.abort("Invalid source type, expected 'file'.")
        ext = os.path.splitext(s_path)[-1].lower()
        # invalid file extension
        if not ext == ".csv":
            utils.abort("Invalid file extension, expected '.csv'")
        # invalid file path
        if not os.path.isfile(s_path):
            utils.abort("Invalid file path, expected existing file")
        
        source = Source(s_lst)

    #tbd        
    elif s_len == 6:
        s_type = s_lst[0]
        s_path = s_lst[1] # odk form/attachment id
        s_proj = s_lst[2] # odk project id
        s_host = s_lst[3] # odk host url
        s_user = s_lst[4] # odk username
        s_pass = s_lst[5] # odk password

        if s_type != "api":
            utils.abort("Invalid source type, expected 'api'.")
        # check API connection & credentials
        # promptAPIcredentials() // host, user, pass, project
        # checkAPIconnection()  // auth endpoint

        source = Source(s_lst)

    return source

def fields(f_str:str, headers=[]):

    f_lst = f_str.split("::", 2)
    f_len = len(f_lst)

    if not f_len in [1,2]:        
        utils.abort("Invalid email/data fields string")
    
    f_email = f_lst[0]

    if f_email not in headers:
        utils.abort(f"Invalid email field '{f_email}'.")

    if f_len == 2:
        f_data = f_lst[1].split(",") 
        for field in f_data:
            if not field in filter(lambda x: x != f_email, headers):
                utils.abort(f"Invalid data field '{field}'")
    
    return Fields(f_lst)

def message(m_str: str):

    m_lst = m_str.split("::", 4)
    m_len = len(m_lst)

    if not m_len == 4:
        utils.abort("Invalid message string, expected [sender]::[format]::[source]::[content]")

    m_sender = m_lst[0]
    m_format = m_lst[1]
    m_source = m_lst[2]
    m_content = m_lst[3]

    # validate message sender
    if not re.match(r"^\S+@\S+\.\S+$", m_sender) :
        raise utils.abort("Invalid message sender. Use valid email address.")
    
    if m_format not in ["txt", "html"]:
        raise utils.abort("Invalid message format. Use either 'txt' or 'html.")
    
    if m_source not in ["stdin", "path"]:
        raise utils.abort("Invalid message source. Use either 'stdin' or 'path.")
    
    # tbd: validate m_content (check if file exists and/or content is valid h)
    
    return Message(m_lst)

def schedule(str: str):
    if str == "now":
        schedule = int(time.time())
    else: 
        # tbd: date format validation
        _datetime = datetime.fromisoformat(str)
        schedule = int(datetime.timestamp(_datetime))

    return Schedule(schedule)

def int_only(_, current):
    re_integer = "^[0-9]*$"
    if not re.search(re_integer, current):
        raise errors.ValidationError('', 'Invalid project id format. Has to be a number')
    return True

def date_format(_, current):
    # tbd: must be future
    re_YYYY_MM_DD_hh_mm = "[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]"
    if not re.search(re_YYYY_MM_DD_hh_mm, current):
        raise errors.ValidationError('', 'Invalid date format. Has to be YYYY-MM-DD hh:mm')       
    return True

def email_address(_, current):
    re_email_address  = "^\S+@\S+\.\S+$"
    if not re.search(re_email_address, current):
        raise errors.ValidationError('', 'Invalid email address format.')
    return True

def not_empty(_, current):
    if current == "":
         raise errors.ValidationError('', 'Content cannot be empty.')
    return True