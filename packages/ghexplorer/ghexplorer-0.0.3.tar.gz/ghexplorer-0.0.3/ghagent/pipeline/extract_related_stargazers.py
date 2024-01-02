from pathlib import Path
import duckdb
import lancedb
from tqdm import tqdm
import pyarrow as pa
from sentence_transformers import SentenceTransformer

from ghagent.util.gharchive import gen_date_list
from ghagent.util.config import EMBEDDING_MODEL_NAME, GHARCHIVE_DIR, LANCEDB_DIR

def get_related_stargazers_from_related_repos(repo: str, target_start_date: str, target_end_date: str):
    dates = gen_date_list(target_start_date, target_end_date)
    db = lancedb.connect(LANCEDB_DIR)
    
    # get all the users who starred the related repos
    print("Getting related repos' stargazers")
    # NOTE: table name doesn't show embedding model yet
    related_repos_table_name = f"{repo.replace('/', '-')}_{target_start_date}_{target_end_date}_related_repos"
    related_repos_table = db.open_table(related_repos_table_name).to_arrow()
    related_repos = duckdb.sql(f"SELECT DISTINCT related_repo AS repo_name FROM related_repos_table;").fetch_arrow_table()
    related_users_sub_tables = []

    for date in tqdm(dates):
        event_file = Path.joinpath(Path(GHARCHIVE_DIR), f"{date}.parquet")
        query = f"SELECT repo.name AS related_repo, repo.url as related_repo_url, actor.login AS related_user, first(created_at) AS created_at FROM '{event_file}' WHERE repo.name IN (SELECT * FROM related_repos) GROUP BY related_repo, related_repo_url, related_user;"
        sub_table = pa.Table.from_pandas(duckdb.sql(query).fetchdf())
        related_users_sub_tables.append(sub_table)
    related_users_table = pa.concat_tables(related_users_sub_tables)
    related_users_table = related_users_table.group_by(["related_repo", "related_repo_url", "related_user"]).aggregate([("created_at", "min")])
    # NOTE: table name doesn't show embedding model yet
    related_users_table_name = f"{repo.replace('/', '-')}_{target_start_date}_{target_end_date}_related_users"
    db.drop_table(related_users_table_name, ignore_missing=True)
    db.create_table(related_users_table_name, related_users_table, schema=pa.schema([
        pa.field("related_repo", pa.utf8()),
        pa.field("related_repo_url", pa.utf8()),
        pa.field("related_user", pa.utf8()),
        pa.field("created_at_min", pa.timestamp('us')),
    ]))

def find_relevant_potential_stargazers(repo: str, target_start_date: str, target_end_date: str, query: str):
    db = lancedb.connect(LANCEDB_DIR)
    repo_info = db.open_table("repo_info")
    related_users = db.open_table(f"{repo.replace('/', '-')}_{target_start_date}_{target_end_date}_related_users").to_arrow()
    if not query.strip():
        repo_info_arrow = repo_info.to_arrow()
    else:
        query_vector = SentenceTransformer(EMBEDDING_MODEL_NAME).encode([query.strip()])[0]
        repo_info_arrow = repo_info.search(query_vector, "description_embedding").to_arrow()
        
    relevant_potential_stargazers = duckdb.sql("SELECT r1.related_user[:20] AS related_user, string_agg(r1.related_repo)[:50] as common_repos, count(r1.related_repo) AS common_repo_cnt FROM related_users r1 JOIN repo_info_arrow r2 ON r1.related_repo = r2.full_name GROUP BY related_user ORDER BY common_repo_cnt DESC LIMIT 1024;").fetch_arrow_table()
    
    return relevant_potential_stargazers.to_pandas()
