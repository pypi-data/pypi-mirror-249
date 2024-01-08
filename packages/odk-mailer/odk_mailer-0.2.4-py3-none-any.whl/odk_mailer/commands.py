import sys
import os
import json
from odk_mailer.lib import prompts, validators, utils, globals, smtp
from odk_mailer.classes.job import Job
from odk_mailer.classes.mailer import Mailer
from odk_mailer.classes.config import Config

def run(hash_or_id, dry=False, verbose=False):

    odk_mailer_config = Config()

    if not odk_mailer_config:
        utils.abort("Cannot send emails without Config")

    if not hash_or_id:
        utils.abort("ID/Hash is required")

    with open(globals.odk_mailer_jobs, "r") as f:
        jobs = json.load(f)

    found = next((obj for obj in jobs if obj["hash"].startswith(hash_or_id)), None)
    if not found:
        utils.abort("Job not found.")

    hash = found['hash']
     
    # check if ready to be sent
    # simple check: scheduled <= now
    # advan. check: hasReminders AND UnsentReminderTime <= now
    
    # if found["scheduled"] > utils.now():
    #     utils.abort("Schedule is in future")

    mailer = Mailer(hash, dry, verbose, odk_mailer_config)
    mailer.send()
    # in case we have a reminder case, generate reminder contents from reminders/hash_reminderId.json

    # update job state: pending, success, errors

def delete(hash):
    if not hash:
            utils.abort("ID is required")

    with open(globals.odk_mailer_jobs, "r") as f:
        jobs = json.load(f)

    found = next((obj for obj in jobs if obj["hash"].startswith(hash)), None)

    if not found:
        utils.abort("Job not found.")
   
    # tbd: confirm
    
    # deletion from /job/<hash>.json
    path_job = os.path.join(globals.odk_mailer_job, found['hash']+'.json')
    if os.path.exists(path_job):
        os.remove(path_job)

    # deletion from /jobs.json
    jobs_updated = list(filter(lambda x: x['hash']!=found['hash'], jobs))   
    
    with open(globals.odk_mailer_jobs, "w") as f:
        f.write(json.dumps(jobs_updated))

    print("Deleted " + found['hash'])


def create(source, fields, message, schedule):

    if not source:
        p_source = prompts.source()
        source  = utils.join(p_source)  # stringify answers
    
    v_source = validators.source(source)

    raw = utils.get_raw(v_source)

    if not fields:
        p_fields = prompts.fields(raw["headers"])
        fields = utils.join(p_fields)

    v_fields = validators.fields(fields, raw["headers"])

    if not message:
        p_message = prompts.message()
        message = utils.join(p_message)

    v_message = validators.message(message)

    if not schedule:
        p_schedule = prompts.schedule()
        if p_schedule["now"]:
            schedule = "now"
        else: schedule=p_schedule["future"]

    v_schedule = validators.schedule(schedule)

    # tbd: Reminders
    # reminders have two attributes:
    # total_amount, frequency, e.g. 3 times in total, every hour|day|week|custom frequency
    # after first scheduled send

    # reminders will be stored inside .odk-mailer/reminder/hash_instance.json
    # having updated recipients from non-respondents (calculated from base recipients and respondents) 
    # on a per reminder case

    # https://github.com/tertek/zapier-odk-scripts/blob/main/get_non_responding.py
    # reminders require api connection and following inputs
    # form_register = "test_form_register" #name of form that is used for registration, given as api or csv
    # form_follow = "test_form_follow"  # name of form that is used for follow up
    # # if use_form_attachment
    # form_follow_attached = "test_form_follow_attached" # name of form that is used for follow up; 
    # form_attachment = "follow.csv" # name of form attachment attached to form_follow; 
    # # field config
    # field_email_register = "email_register" # name of email field for registration form, given
    # field_email_follow = "email_follow"
    # field_email_follow_attach = "email"

    job = Job(v_source, v_fields, v_message, v_schedule, raw)
    
    if "pytest" in sys.modules:
        # testing
        print(vars(job))
        sys.exit()
        
    saved = job.save()

    print()
    print("Created " + saved["hash"])
    print()

    # validate recipients and process invalid emails in case
    # if not recipients.validate(email_field):
    #     utils.render_table(["id", "email_field", "error"], recipients.invalidEmails)
    #     ignore_invalid_emails = typer.confirm("Invalid emails found. Would you like to continue although you have invalid emails?")
    
    #     if not ignore_invalid_emails:
    #         raise typer.Exit("\nAborted.")
    # store mail-tasks in a text file or JSON https://www.w3schools.com/python/python_json.asp
    # https://stackoverflow.com/a/24608746/3127170
    # the task will be stored with final data

    # task = {
    #   csv_file: path/to/file.csv
    #   email_field: email
    #   message: <msg>
    #   sender: <sndr>
    #   reminders: ...
    # }
        
    # add cron-job via https://pypi.org/project/python-crontab/ and https://stackabuse.com/scheduling-jobs-with-python-crontab/
    # We will need a single job, that checks every hour if we have open jobs (with reminder tasks.)
    # Process reminder tasks as follows: 
    # 1. Perform API request to calculate reminder recipients
    # 2. Send Emails based on calculated recipients
    # 3. Summarize progress


    #
    # odk-mailer run command <hash>
    #

    # 1. check if job exists under <hash>
    # 2. get job details
    # 3. replace placeholder in message with data (python template engine)
    # 4. 

def list_jobs():

    with open(globals.odk_mailer_jobs, "r+") as f:
        jobs = json.load(f)

    utils.print_jobs(jobs)


def evaluate(dry=False):

    with open(globals.odk_mailer_jobs, "r+") as f:
        jobs = json.load(f)

    evals = []

    for job in jobs:
        if job["scheduled"] <= utils.now():
            # simple evaluation: check if scheduled time is smaller/equal to now
            # if true, add to selected list
            evals.append(job["hash"])

        ###
        # untested code, since reminders are not yet implemented in create command
        elif "reminders" in job and len(job["reminders"]) > 0:
            # advanced evaluation: addtionally check if job has reminder times that are smaller/equal to now
            # if true, add to selected list
            print("Addiitonally checking if we have any valid reminders")
            for reminder in job["reminders"]:
                if reminder["timestamp"] <= utils.now():
                    evals.append(job["hash"])
                    break
        ###
                
        else:
            # skipping this job since not qualified to be run
            pass

    if dry:
        print(evals)
        print(len(evals))

    else:
        for eval in evals:
            run(eval)

def test(sender, recipient, host, port):
    print()
    print(f"Sending test mail from {sender} to:  {recipient} via: {host}:{port}")
    print()
    smtp.send_mail(sender, recipient, host, port)