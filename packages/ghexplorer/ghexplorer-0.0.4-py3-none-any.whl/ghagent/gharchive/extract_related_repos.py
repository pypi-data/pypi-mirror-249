#%%
import csv
import sys
import duckdb
from pathlib import Path
from tqdm import tqdm

DATA_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics")
ANALYTICS_DIR = Path.joinpath(DATA_DIR, "analytics")
USER_INFO_FILE = Path.joinpath(DATA_DIR, "user_info.csv")
WATCH_EVENTS_FILE = Path.joinpath(DATA_DIR, "watch_events.csv")
MISSING_USERS_FILE = Path.joinpath(DATA_DIR, "missing_users.csv")

def extract_related_repos(repo:str):
    con = duckdb.connect()
    query = f"""
SELECT DISTINCT r2.repo_full_name, r1.stargazer_login AS common_stargazer, r1.created_at as create_at
FROM '{WATCH_EVENTS_FILE}' r1
JOIN '{WATCH_EVENTS_FILE}' r2 ON r1.stargazer_login = r2.stargazer_login
WHERE r1.repo_full_name = '{repo}' AND r2.repo_full_name <> '{repo}';
""".strip()
    repo_stargazers = con.execute(query).fetchall()
    with open(f"{ANALYTICS_DIR}/related_repos_{repo.replace('/', '-')}.csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["repo_full_name", "common_stargazer", "created_at"])
        writer.writerows(repo_stargazers)
    con.close()

def extract_related_watch_events(repo:str):
    con = duckdb.connect()
    related_repos_file = f"{ANALYTICS_DIR}/related_repos_{repo.replace('/', '-')}.csv"
    related_watch_events_file = f"{ANALYTICS_DIR}/related_watch_events_{repo.replace('/', '-')}.csv"
    query = f"""
SELECT * FROM '{WATCH_EVENTS_FILE}'
WHERE repo_full_name in (SELECT repo_full_name FROM '{related_repos_file}');
""".strip()
    related_watch_events = con.execute(query).fetchall()
    with open(related_watch_events_file, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["stargazer_login", "stargazer_url", "repo_full_name", "repo_url", "created_at"])
        writer.writerows(related_watch_events)
    con.close()

repo = "litanlitudan/skyagi"
# extract_related_repos(repo)
# extract_related_watch_events(repo)
