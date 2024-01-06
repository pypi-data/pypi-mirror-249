import os
import json
from odk_mailer.lib import utils
from types import SimpleNamespace
# https://stackoverflow.com/questions/24608665/how-to-store-python-application-data/24608746#24608746


# loads and validates config from JSON file
def load_config():
    with open(os.path.join(odk_mailer_base, "config.json"), "r") as f:
        config = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
        #config = json.load(f)
    
    if not config:
        utils.abort("Config Error: Check .odk-mailer/config.json ")

    required_keys = ["odk_host", "smtp_host", "smtp_port"]

    for required_key in required_keys:
        if not required_key in vars(config):
            utils.abort(f"Invalid config: Key '{required_key}' is required.")

    return config


odk_mailer_base = os.path.join(os.getenv("HOME"), ".odk-mailer")
odk_mailer_jobs = os.path.join(odk_mailer_base, "jobs.json")
odk_mailer_job = os.path.join(odk_mailer_base, "job")
path_config = os.path.join(odk_mailer_base, "config.json")
#odk_mailer_path = os.path.expanduser('~') + "/.odk-mailer"

odk_mailer_config = load_config()


