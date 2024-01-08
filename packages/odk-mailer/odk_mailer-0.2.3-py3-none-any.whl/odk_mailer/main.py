import typer
from typing import Optional
from typing_extensions import Annotated
from odk_mailer import commands, before

app = typer.Typer(
    add_completion=False, 
    pretty_exceptions_enable=True
)

@app.callback()
def callback():
    """
    ODK Mailer

    Setup mail jobs by fetching recipients from CSV files or ODK API.

    Run mail jobs immediately or schedule them to be run over time.

    Automatically send reminders to non-responding mail recipients.
    """
    # read config here from $HOME/.odk-mailer
    before.init()

@app.command()
def create(
    source: Annotated[Optional[str], typer.Option("--source", "-s", help="Define source as [type]::[path]")]= "",
    fields: Annotated[Optional[str], typer.Option("--fields", "-f", help="Define fields as [email]::[field_1],[field_2]")]= "",
    message: Annotated[Optional[str], typer.Option("--message", "-m", help="Define message as [sender]::[format]::[type]::[content]")]= "",
    schedule: Annotated[Optional[str], typer.Option("--schedule", help="Define schedule as 'now' or [time] in YYYY-MM-DD HH:mm")]= "",
):
    """
    Create mail job
    """
    commands.create(source, fields, message, schedule)

@app.command()
def run(
    id: Annotated[str, typer.Argument(help="Hexadecimal hash")],
    dry: Annotated[bool, typer.Option("--dry", help="Dry run without sending mails.")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", help="Print out smtp debugging information")] = False,
):
    """
    Run mail job
    """
    commands.run(id, dry, verbose)

@app.command()
def delete(
    id: Annotated[str, typer.Argument(help="Hexadecimal hash")]
):
    """
    Delete mail job
    """
    commands.delete(id)

@app.command()
def list():
    """
    List mail jobs
    """    
    commands.list_jobs()

@app.command()
def evaluate(
    dry: Annotated[bool, typer.Option("--dry", help="Dry run without sending mails.")] = False
):
    """
    Evaluate mail jobs
    """
    commands.evaluate(dry)

@app.command()
def test():
    """
    Test STMP connection
    """
    commands.test()

# @app.command()
# def config():
#     """
#     Configure ODK Mailer
#     """
#     typer.echo("Open configuration dialog if no config")
# @app.command()
# def api():
#     """
#     Send api request
#     """
#     typer.echo("api call")

#     odk_client = ODKClient()

#     # odk_client.auth()

#     # odk_client.submissions_data()

#     odk_client.form_attachment()



