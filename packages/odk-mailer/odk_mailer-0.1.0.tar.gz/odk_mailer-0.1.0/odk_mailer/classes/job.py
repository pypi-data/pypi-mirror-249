from odk_mailer.lib import globals
from datetime import datetime
import time
import json
import hashlib
from enum import Enum
import os

class JobType(Enum):
    FILE = 'file'
    API = 'api'

class Source:
    type: str
    path: str
    project: int
    hostname: str
    username: str
    password: str

    def __init__(self, lst: []):
        if not len(lst) in [2,6]: 
            raise Exception("Source input must have length 2 or 6.")
        
        self.type = JobType(lst[0]).value
        self.path = lst[1]
        if len(lst) == 6:
            self.project = int(lst[2])
            self.hostname = lst[3]
            self.username = lst[4]
            self.password = lst[5]

class Fields:
    email: str
    data: []

    def __init__(self, lst: []):
        if not len(lst) in [1,2]:
            raise Exception("Fields input must have length 1 or 2.")
        
        self.email = lst[0]
        # data fields are optional
        if len(lst) == 2:
            self.data = lst[1].split(",")

class Message:
    sender: str
    format: str
    source: str
    content: str

    def __init__(self, lst: []):
        if not len(lst) == 4:
            raise Exception("Message input must have length 4.")
                
        self.sender = lst[0]
        self.format = lst[1]
        self.source = lst[2]
        self.content = lst[3]        

class Schedule:
    timestamp: int

    def __init__(self,int:int):
        self.timestamp = int

class Job:
    created: int
    source: Source
    fields: Fields
    message: Message
    schedule: Schedule
    recipients: []
    json: str
    hash: str

    def __init__(self, source:Source, fields:Fields, message:Message, schedule:Schedule, raw:{}):

        self.created = int(time.time())
        self.source = vars(source)
        self.fields = vars(fields)
        self.message = vars(message)
        self.schedule = schedule.timestamp

        self.setRecipients(raw)
        self.setJSON()
        self.setHash()

    def setRecipients(self, data):
        recipients = []
        for row in data["rows"]:
            f_row = {k: row[k] for k in self.fields["data"] + [self.fields["email"]]}
            recipients.append(f_row)
        self.recipients = recipients

    def setJSON(self):
        self.json = json.dumps(vars(self), ensure_ascii=True, indent=4)

    def setHash(self):
        self.hash = hashlib.sha256(self.json.encode()).hexdigest()

    # does two things: saves mailjob as <hash>.json 
    # and adds it as an entry to jobs.json with hash as id
    def save(self):

        # save files
        path_to_job = os.path.join(globals.odk_mailer_job, self.hash+'.json')
        with open(path_to_job, 'w', encoding='utf-8') as f:
            f.write(self.json)

        with open(globals.odk_mailer_jobs, "r+") as f:
            jobs = json.load(f)
            save_job = {
                "hash": self.hash,
                "scheduled": self.schedule, 
                "created": self.created,
                "state":0
            }
            jobs.append(save_job)
            f.seek(0)
            f.truncate()
            f.write(json.dumps(jobs))

        return save_job
