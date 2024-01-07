#%%
import csv
import sys
import duckdb
from pathlib import Path
from tqdm import tqdm

DATA_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics")
USER_INFO_FILE = Path.joinpath(DATA_DIR, "user_info.csv")
WATCH_EVENTS_FILE = Path.joinpath(DATA_DIR, "watch_events.csv")
MISSING_USERS_FILE = Path.joinpath(DATA_DIR, "missing_users.csv")

def extract_missing_users():
    con = duckdb.connect()
    users = con.execute(f"SELECT DISTINCT stargazer_login, stargazer_url from '{WATCH_EVENTS_FILE}';").fetchall()
    fetched_users = con.execute(f"SELECT login from '{USER_INFO_FILE}';").fetchall()
    fetched_user_logins = set([user[0] for user in fetched_users])
    missed_users = []
    for user in tqdm(users):
        if user[0] not in fetched_user_logins:
            missed_users.append(user)
    with open(MISSING_USERS_FILE, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["user_login", "user_url"])
        writer.writerows(missed_users)
    con.close()

extract_missing_users()
