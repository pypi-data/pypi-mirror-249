import os
from ghagent.tui import GHAgentApp
from ghagent.util.conversion import df_to_rich_table
import typer
import json
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from rich import box

from ghagent.util.gharchive import fetch_events, get_event_dates_to_download
from ghagent.util.io import load_json_value
from ghagent.util.config import CONFIG_FILE_PATH, GHAGENT_HOME, GHARCHIVE_DIR, set_github_token, set_time_window, ConfigValidationError, config_validation_check
from ghagent.pipeline.extract_related_repos import find_relevant_related_repos, get_related_repos
from ghagent.pipeline.extract_related_stargazers import find_relevant_potential_stargazers, get_related_stargazers_from_related_repos
from ghagent.pipeline.encode_related_repos import fetch_related_repo_info


cli = typer.Typer()
console = Console()

#######################################################################################
# Config CLI

config_cli = typer.Typer()

@config_cli.command("timewindow")
def config_timewindow():
    """
    Configure the time window for the app
    """
    console.print("Configuring time window...")
    target_start_date = load_json_value(CONFIG_FILE_PATH, "start_date", "")
    target_end_date = load_json_value(CONFIG_FILE_PATH, "end_date", "")
    console.print(f"Current time window: from {target_start_date} to {target_end_date}")
    
    start_date = Prompt.ask("Please input the start date of the time window, in format YYYY-MM-DD", default="2023-05-01")
    end_date = Prompt.ask("Please input the end date of the time window, in format YYYY-MM-DD", default="2023-05-01")
    
    try:
        set_time_window(start_date=start_date, end_date=end_date)
    except FileNotFoundError as e:
        console.print("Didn't find config file, run `gha init` to initialize.")
    
@config_cli.command("token")
def config_token():
    """
    Configure the github API token
    """
    console.print("Configuring Github token...")
    token = Prompt.ask("Please enter your Github API token")

    try:
        set_github_token(token)
    except FileNotFoundError as e:
        console.print("Didn't find config file, run `gha init` to initialize.")
    
@config_cli.callback(no_args_is_help=True)
def main(ctx: typer.Context):
    """
    Configuration
    """

cli.add_typer(config_cli, name="config")

#######################################################################################
# Main CLI

@cli.callback(no_args_is_help=True)
def main(ctx: typer.Context):
    """
    """
    pass


@cli.command()
def run(repo: str, output_format: str = "textual"):
    """
    Run the GHAgent for a given repository
    """
    print(f"Running GHAgent for {repo}...")
    
    # sanity check
    try:
        config_validation_check()
    except ConfigValidationError as e:
        if e.status_code == 1001:
            console.print("[red]Didn't find config file, please run `gha init` to initialize.")
        elif e.status_code == 1002:
            console.print("[red]Didn't have explicit start or end date set, please run `gha config timewindow` to specify properly.")
        elif e.status_code == 1003:
            console.print("[red]Didn't find GitHub API Access Token, please run `gha config token` to specify properly.")
        return

    # Fetch Events
    target_start_date = load_json_value(CONFIG_FILE_PATH, "start_date", "")
    target_end_date = load_json_value(CONFIG_FILE_PATH, "end_date", "")
    console.print(f"Configed time window: from {target_start_date} to {target_end_date}")
    if len(target_start_date) == 0 or len(target_end_date) == 0:
        console.print(f"Start date or end date is empty, please specify them by running `gha config timewindow` properly.")
    confirm = Prompt.ask("Please confirm the time window, do you want to continue? (y/n)", choices=["y", "n"], default="y")
    if confirm == "n":
        return
    
    event_dates_to_download = get_event_dates_to_download(target_start_date=target_start_date, target_end_date=target_end_date, output_dir=GHARCHIVE_DIR)
    if len(event_dates_to_download) > 0:
        console.print(f"{len(event_dates_to_download)} dates' data are not found locally, which need to download remotely: {event_dates_to_download}")

        ## Prompt to ask if the user wants to fetch the data
        confirm = Prompt.ask("Do you want to download the data? (y/n)", choices=["y", "n"], default="y")
        if confirm == "y":
            fetch_events(event_dates_to_download, output_dir=GHARCHIVE_DIR)
        else:
            return
    
    # Create the related repos table in lancedb
    get_related_repos(repo=repo, target_start_date=target_start_date, target_end_date=target_end_date)
    
    # Create the related stargazers table in lancedb
    get_related_stargazers_from_related_repos(repo=repo, target_start_date=target_start_date, target_end_date=target_end_date)
    
    # Calculate the embeddings of repo's name and description, and save them to `repo_info` table in lancedb
    fetch_related_repo_info(repo=repo, target_start_date=target_start_date, target_end_date=target_end_date)
    
    # Get the query from the user to filter
    while True:
        query = Prompt.ask("Please input your query to filter relevant related repos and potential stargazers, leave it empty if you don't have any query", default="")
        
        # Find relevant related repos
        relevant_related_repos = find_relevant_related_repos(repo=repo, target_start_date=target_start_date, target_end_date=target_end_date, query=query)
        
        # Find relevant potential stargazers
        relevant_potential_stargazers = find_relevant_potential_stargazers(repo=repo, target_start_date=target_start_date, target_end_date=target_end_date, query=query)
        
        # Show the final result to the user
        if output_format == "textual":
            app = GHAgentApp(relevant_related_repos=relevant_related_repos, potential_stargazers=relevant_potential_stargazers)
            app.run()
        elif output_format == "rich":
            console.print("Related Repos", style="bold cyan")
            relevant_related_repos_table = Table(show_header=True, header_style="bold magenta")
            relevant_related_repos_table = df_to_rich_table(relevant_related_repos, relevant_related_repos_table)
            relevant_related_repos_table.row_styles = ["none", "dim"]
            relevant_related_repos_table.box = box.SIMPLE_HEAD
            console.print(relevant_related_repos_table)
            
            console.print("Potential Stargazers", style="bold cyan")
            relevant_potential_stargazers_table = Table(show_header=True, header_style="bold magenta")
            relevant_potential_stargazers_table = df_to_rich_table(relevant_potential_stargazers, relevant_potential_stargazers_table)
            relevant_potential_stargazers_table.row_styles = ["none", "dim"]
            relevant_potential_stargazers_table.box = box.SIMPLE_HEAD
            console.print(relevant_potential_stargazers_table)
            
        # Ask users if they want to start a new query
        confirm = Prompt.ask("Do you want to try a new query? (y/n)", choices=["y", "n"], default="y")
        
        if confirm == "n":
            break

@cli.command()
def init():
    """
    Initialize the GHAgent environment at ~/.ghagent
    ~/.ghagent/gharchive/: 2020-01-01.parquet, 2020-01-02.parquet, ...
    """
    print("Initializing GHAgent environment...")
    # Create ~/.ghagent if not exists
    if not os.path.exists(GHAGENT_HOME):
        os.makedirs(GHAGENT_HOME)
    # Create ~/.ghagent/config.json if not exists
    if not os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "w") as f:
            json.dump({}, f)
