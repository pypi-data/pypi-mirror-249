from odk_mailer.lib import globals
import os
import json

def getJobs():
    with open(globals.odk_mailer_jobs, "r") as f:
        jobs = json.load(f)
    
    return jobs

def getJob(hash):
    path_jobs = os.path.join(globals.odk_mailer_job, hash+'.json')
    with open(path_jobs, 'r', encoding='utf-8') as f:
        job = json.load(f)

    return job



