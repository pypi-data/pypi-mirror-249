from pathlib import Path
from odk_mailer.lib import globals
import typer
import json

def init():

  # create base dir if not exists
  path_base = Path(globals.odk_mailer_base)
  path_base.mkdir(parents=True, exist_ok=True)
  
  # create config.json if not exists
  path_config  =  Path(globals.path_config)
  if not path_config.exists():
      path_config.touch()

  if path_config.stat().st_size == 0:
      path_config.write_text("{}")

  if not is_json(path_config.read_text()):
      raise typer.Exit("The config.json file is invalid.\n" + path_config)        

  # create job dir if not exists
  path_job = Path(globals.odk_mailer_job)
  path_job.mkdir(parents=True, exist_ok=True)

  # create jobs.json if not exists
  path_jobs = Path(globals.odk_mailer_jobs)

  if not path_jobs.exists():
      path_jobs.touch()

  if path_jobs.stat().st_size == 0:
      path_jobs.write_text("[]")

  if not is_json(path_jobs.read_text()):
      raise typer.Exit("The jobs.json file is invalid.\n" + path_jobs)
  

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True