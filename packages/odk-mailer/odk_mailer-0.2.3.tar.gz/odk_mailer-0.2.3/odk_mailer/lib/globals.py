import os

# global variables
odk_mailer_base = os.path.join(os.getenv("HOME"), ".odk-mailer")
odk_mailer_jobs = os.path.join(odk_mailer_base, "jobs.json")
odk_mailer_job = os.path.join(odk_mailer_base, "job")
path_config = os.path.join(odk_mailer_base, "config.json")


# # will be set in before
# odk_mailer_config = {}