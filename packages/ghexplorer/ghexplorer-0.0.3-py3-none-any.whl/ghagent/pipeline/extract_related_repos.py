#%%
import csv
import sys
import duckdb
from pathlib import Path
from tqdm import tqdm
import lancedb
import pyarrow as pa
from sentence_transformers import SentenceTransformer

from ghagent.util.config import EMBEDDING_MODEL_NAME, GHARCHIVE_DIR, LANCEDB_DIR
from ghagent.util.gharchive import gen_date_list

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


def get_related_repos(repo: str, target_start_date: str, target_end_date: str):
    dates = gen_date_list(target_start_date, target_end_date)
    db = lancedb.connect(LANCEDB_DIR)

    # step 1: get repo's all stargazers
    print("Getting repo's stargazers")
    stargazer_logins = set()
    for date in tqdm(dates):
        event_file = Path.joinpath(Path(GHARCHIVE_DIR), f"{date}.parquet")
        query = f"SELECT DISTINCT actor.login as login FROM '{event_file}' WHERE type = 'WatchEvent' AND repo.name = '{repo}';"
        stargazer_logins.update(duckdb.sql(query).fetchdf()["login"].tolist())
    stargazer_logins = pa.Table.from_arrays([pa.array(list(stargazer_logins), pa.utf8())], names=["login"])

    # step 2: get all the repos that the repo's stargazersers starred
    print("Getting stargazers' starred repos")
    related_repos_sub_tables = []
    for date in tqdm(dates):
        event_file = Path.joinpath(Path(GHARCHIVE_DIR), f"{date}.parquet")
        query = f"SELECT repo.name AS related_repo, repo.url as related_repo_url, actor.login AS common_stargazer, first(created_at) AS created_at FROM '{event_file}' WHERE actor.login IN (SELECT * FROM stargazer_logins) GROUP BY related_repo, related_repo_url, common_stargazer;"
        sub_table = pa.Table.from_pandas(duckdb.sql(query).fetchdf())
        related_repos_sub_tables.append(sub_table)
    related_repos_table = pa.concat_tables(related_repos_sub_tables)
    related_repos_table = related_repos_table.group_by(["related_repo", "related_repo_url", "common_stargazer"]).aggregate([("created_at", "min")])
    # NOTE: table name doesn't show embedding model yet
    related_repos_table_name = f"{repo.replace('/', '-')}_{target_start_date}_{target_end_date}_related_repos"
    db.drop_table(related_repos_table_name, ignore_missing=True)
    db.create_table(related_repos_table_name, related_repos_table, schema=pa.schema([
        pa.field("related_repo", pa.utf8()),
        pa.field("related_repo_url", pa.utf8()),
        pa.field("common_stargazer", pa.utf8()),
        pa.field("created_at_min", pa.timestamp('us')),
    ]))

def find_relevant_related_repos(repo: str, target_start_date: str, target_end_date: str, query: str):
    db = lancedb.connect(LANCEDB_DIR)
    repo_info = db.open_table("repo_info")
    related_repos = db.open_table(f"{repo.replace('/', '-')}_{target_start_date}_{target_end_date}_related_repos").to_arrow()
    if not query.strip():
        repo_info_arrow = repo_info.to_arrow()
    else:
        query_vector = SentenceTransformer(EMBEDDING_MODEL_NAME).encode([query.strip()])[0]
        repo_info_arrow = repo_info.search(query_vector, "description_embedding").to_arrow()
        
    relevant_related_repos = duckdb.sql("SELECT r1.related_repo[:50] AS related_repo, r2.description[:50] AS description, string_agg(r1.common_stargazer)[:20] AS common_stargazers, count(r1.common_stargazer) AS common_stargazer_cnt FROM related_repos r1 JOIN repo_info_arrow r2 ON r1.related_repo = r2.full_name GROUP BY related_repo, description ORDER BY common_stargazer_cnt DESC LIMIT 1024;").fetch_arrow_table()
    
    return relevant_related_repos.to_pandas()
