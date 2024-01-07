#%%
import csv
import sys
import duckdb
from pathlib import Path
from tqdm import tqdm

DATA_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics")
REPO_INFO_FILE = Path.joinpath(DATA_DIR, "repo_info.csv")
WATCH_EVENTS_FILE = Path.joinpath(DATA_DIR, "watch_events.csv")
MISSING_REPOS_FILE = Path.joinpath(DATA_DIR, "missing_repos.csv")

def extract_missing_repos():
    con = duckdb.connect()
    repos = con.execute(f"SELECT DISTINCT repo_full_name, repo_url from \"{WATCH_EVENTS_FILE}\";").fetchall()
    fetched_repos = con.execute(f"SELECT full_name from \"{REPO_INFO_FILE}\";").fetchall()
    fetched_repo_names = set([repo[0] for repo in fetched_repos])
    missed_repos = []
    for repo in tqdm(repos):
        if repo[0] not in fetched_repo_names:
            missed_repos.append(repo)
    with open(MISSING_REPOS_FILE, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["repo_full_name", "repo_url"])
        writer.writerows(missed_repos)
    con.close()

extract_missing_repos()
