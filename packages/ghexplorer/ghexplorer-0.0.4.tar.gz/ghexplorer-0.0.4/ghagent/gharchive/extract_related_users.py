#%%
from typing import List
import duckdb
import lancedb
import pyarrow as pa
from sentence_transformers import SentenceTransformer
from pathlib import Path
from tqdm import tqdm

DATA_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics")
CACHE_DB = Path.joinpath(DATA_DIR, "cache/cache.db")
# GITHUB_EVENTS_DIR = Path.joinpath(Path.home(), "nfs/datasets/github-events")
GITHUB_EVENTS_DIR = Path.joinpath(DATA_DIR, "github_events")
RELATED_USERS_DIR = Path.joinpath(DATA_DIR, "related_users")
RELATED_REPOS_DIR = Path.joinpath(DATA_DIR, "related_repos")
LANCEDB_DIR = Path.joinpath(DATA_DIR, "vectordb/github_analytics")
MODEL_NAME="all-MiniLM-L6-v2"
MODEL = SentenceTransformer(MODEL_NAME)
EMBEDDING_SIZE = 384

def get_all_event_dates() -> List[str]:
    dates = []
    for file in GITHUB_EVENTS_DIR.glob("*.parquet"):
        dates.append(file.name.split(".")[0])
    dates.sort()
    return dates

def extract_related_users(repo:str):
    dates = get_all_event_dates()
    db = lancedb.connect(LANCEDB_DIR)
    # step 1: get repo's all stargazers
    print("Getting repo's stargazers")
    stargazer_logins = set()
    for date in tqdm(dates):
        event_file = Path.joinpath(GITHUB_EVENTS_DIR, f"{date}.parquet")
        query = f"SELECT DISTINCT actor.login as login FROM '{event_file}' WHERE type = 'WatchEvent' AND repo.name = '{repo}';"
        stargazer_logins.update(duckdb.sql(query).fetchdf()["login"].tolist())
    stargazer_logins = pa.Table.from_arrays([pa.array(list(stargazer_logins), pa.utf8())], names=["login"])
    # step 2: get all the repos that the repo's stargazersers starred
    print("Getting stargazers' starred repos")
    related_repos_sub_tables = []
    for date in tqdm(dates):
        event_file = Path.joinpath(GITHUB_EVENTS_DIR, f"{date}.parquet")
        query = f"SELECT repo.name AS related_repo, actor.login AS common_stargazer, first(created_at) AS created_at FROM '{event_file}' WHERE actor.login IN (SELECT * FROM stargazer_logins) GROUP BY related_repo, common_stargazer;"
        sub_table = pa.Table.from_pandas(duckdb.sql(query).fetchdf())
        related_repos_sub_tables.append(sub_table)
    related_repos_table = pa.concat_tables(related_repos_sub_tables)
    related_repos_table = related_repos_table.group_by(["related_repo", "common_stargazer"]).aggregate([("created_at", "min")])
    related_repos_table_name = f"{repo.replace('/', '-')}_related_repos"
    db.drop_table(related_repos_table_name, ignore_missing=True)
    db.create_table(related_repos_table_name, related_repos_table)
    # step 3: get all the users who starred the repos
    print("Getting related repos' stargazers")
    related_repos = duckdb.sql("SELECT DISTINCT related_repo AS repo_name FROM related_repos_table;").fetch_arrow_table()
    related_users_sub_tables = []
    for date in tqdm(dates):
        event_file = Path.joinpath(GITHUB_EVENTS_DIR, f"{date}.parquet")
        query = f"SELECT repo.name AS related_repo, actor.login AS related_user, first(created_at) AS created_at FROM '{event_file}' WHERE repo.name IN (SELECT * FROM related_repos) GROUP BY related_repo, related_user;"
        sub_table = pa.Table.from_pandas(duckdb.sql(query).fetchdf())
        related_users_sub_tables.append(sub_table)
    related_users_table = pa.concat_tables(related_users_sub_tables)
    related_users_table = related_users_table.group_by(["related_repo", "related_user"]).aggregate([("created_at", "min")])
    related_users_table_name = f"{repo.replace('/', '-')}_related_users"
    db.drop_table(related_users_table_name, ignore_missing=True)
    db.create_table(related_users_table_name, related_users_table)

def query_related_users(repo: str, query: str):
    db = lancedb.connect(LANCEDB_DIR)
    repo_info = db.open_table("repo_info")
    if not query.strip():
        relevant_repos = repo_info.to_arrow()
    else:
        query_vector = MODEL.encode([query])[0]
        relevant_repos = repo_info.search(query_vector, "description_embedding").to_arrow()
    related_users = db.open_table(f"{repo.replace('/', '-')}_related_users").to_arrow()
    query = "SELECT related_repo, STRING_AGG(related_user), COUNT(related_user) FROM related_users WHERE related_repo IN (SELECT full_name FROM relevant_repos) GROUP BY related_repo;"
    all_relevant_related_repo_user = duckdb.sql(query).fetchall()
    return all_relevant_related_repo_user

extract_related_users("litanlitudan/skyagi")
# extract_related_users('unx21/violet')
# query_related_users('unx21/violet', 'hmm')
# repo = "unx21/violet"
# %%
