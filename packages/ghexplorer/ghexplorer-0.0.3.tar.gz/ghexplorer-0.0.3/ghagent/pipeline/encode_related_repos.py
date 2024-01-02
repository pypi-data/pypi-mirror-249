import duckdb
import lancedb
import shutil
import pandas as pd
import pyarrow as pa
import requests
from sentence_transformers import SentenceTransformer
from pathlib import Path
from tqdm import tqdm

from ghagent.util.io import load_json_value
from ghagent.util.config import CONFIG_FILE_PATH, LANCEDB_DIR, ConfigValidationError

REPO_DB_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics/vectordb/repo_info")
REPO_FILE = Path.joinpath(Path.home(), "data/github_archive_analytics/updated_expanded_repo_info.parquet")
BATCH_SIZE = 128
MICRO_BATCH_SIZE = 128 # used for GPU processing

MODEL_NAME="all-MiniLM-L6-v2"
MODEL = SentenceTransformer(MODEL_NAME)
EMBEDDING_SIZE = 384

def fetch_related_repo_info(repo: str, target_start_date: str, target_end_date: str):
    # get all related repos' urls from table
    db = lancedb.connect(LANCEDB_DIR)
    related_repos = db.open_table(f"{repo.replace('/', '-')}_{target_start_date}_{target_end_date}_related_repos").to_arrow()
    get_all_repos_urls_query = "SELECT DISTINCT related_repo_url FROM related_repos;"
    repo_urls = duckdb.sql(get_all_repos_urls_query).fetchall()
    
    # only request to urls that are not in `repo_info` table
    try:
        repo_info_tbl = db.open_table("repo_info")
        repo_info_tbl_arrow = repo_info_tbl.to_arrow()
        # NOTE: use single quote: https://stackoverflow.com/a/75671555
        repo_urls = [repo_url for repo_url in repo_urls if int(duckdb.sql(f"""SELECT COUNT(*) FROM repo_info_tbl_arrow WHERE repo_url = '{repo_url[0]}';""").fetchone()[0]) == 0]
    except FileNotFoundError as e:
        # since there is no `repo_info` table, all urls should be requested
        pass
    
    # request to urls to get repo's info
    access_token = load_json_value(CONFIG_FILE_PATH, "github_token", "")
    if not access_token:
        raise ConfigValidationError("Github Access Token is not set", 1003)
    headers = {
        "Authorization": f"token {access_token}",
    }
    repo_infos = []

    pbar = tqdm(repo_urls)
    for repo_url in pbar:
        pbar.set_description(f"Fetching {repo_url[0]}")

        try:
            response = requests.get(repo_url[0], headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # NOTE: should handle the exception properly
            print(f"Failed to request to GitHub API, reason: {response.text}")
            continue
        
        repo_info = response.json()
        repo_infos.append({
            "id": repo_info["id"],
            "description": repo_info["description"],
            "name": repo_info["name"],
            "full_name": repo_info["full_name"],
            "repo_url": repo_url[0],
        })
    
    # calculate the embeddings
    for batch in tqdm(range(len(repo_infos) // MICRO_BATCH_SIZE + 1)):
        start = batch * MICRO_BATCH_SIZE
        end = (batch + 1) * MICRO_BATCH_SIZE
        if start >= len(repo_infos):
            break
        if end > len(repo_infos):
            end = len(repo_infos)

        description_embeddings = MODEL.encode([repo_info["description"] for repo_info in repo_infos[start:end]], batch_size=MICRO_BATCH_SIZE)
        description_embeddings = [embedding.tolist() for embedding in description_embeddings]
        name_embeddings = MODEL.encode([repo_info["name"] for repo_info in repo_infos[start:end]], batch_size=MICRO_BATCH_SIZE)
        name_embeddings = [embedding.tolist() for embedding in name_embeddings]
        
        for i in range(start, end):
            repo_infos[i]["description_embedding"] = description_embeddings[i - start]
            repo_infos[i]["name_embedding"] = name_embeddings[i - start]

    # save the repo infos to `repo_info` table
    try:
        repo_info_tbl = db.open_table("repo_info")
        repo_info_tbl_arrow = repo_info_tbl.to_arrow()
        for repo_info in tqdm(repo_infos):
            is_exist = int(duckdb.sql(f'SELECT COUNT(*) FROM repo_info_tbl_arrow WHERE id = {repo_info["id"]};').fetchone()[0]) > 0
            if is_exist:
                # workaroud: duckdb's update operation has unresolved error
                # repo_info_tbl.update(where=f'id = {repo_info["id"]}', values=repo_info)
                repo_info_tbl.delete(where=f'id = {repo_info["id"]}')

            repo_info_tbl.add([repo_info])
    except FileNotFoundError as e:
        # create new table
        schema = pa.schema([
            pa.field("id", pa.int64()),
            pa.field("description", pa.utf8()),
            pa.field("name", pa.utf8()),
            pa.field("full_name", pa.utf8()),
            pa.field("repo_url", pa.utf8()),
            pa.field("description_embedding", pa.list_(pa.float32(), EMBEDDING_SIZE)),
            pa.field("name_embedding", pa.list_(pa.float32(), EMBEDDING_SIZE)),
        ])
        
        if len(repo_infos) == 0:
            # create empty table
            db.create_table("repo_info", schema=schema)
        else:
            db.create_table("repo_info", repo_infos, schema=schema)

def create_repo_info_table():
    db = lancedb.connect(REPO_DB_DIR)
    con = duckdb.connect()

    schema = pa.schema([
        pa.field("id", pa.int64()),
        pa.field("description", pa.utf8()),
        pa.field("name", pa.utf8()),
        pa.field("full_name", pa.utf8()),
        pa.field("description_embedding", pa.list_(pa.float32(), EMBEDDING_SIZE)),
        pa.field("name_embedding", pa.list_(pa.float32(), EMBEDDING_SIZE))
    ])

    repo_count = con.execute(f"select count(*) from '{REPO_FILE}';").fetchone()[0]
    
    def make_batches():
        query = con.execute(f"""select id, name, full_name, description from '{REPO_FILE}';""")
        for batch in tqdm(query.fetch_record_batch(BATCH_SIZE), total=(repo_count // BATCH_SIZE)):
            description_embeddings = MODEL.encode(batch["description"].to_pylist(), batch_size=MICRO_BATCH_SIZE)
            description_embeddings = [embedding.tolist() for embedding in description_embeddings]
            name_embeddings = MODEL.encode(batch["name"].to_pylist(), batch_size=MICRO_BATCH_SIZE)
            name_embeddings = [embedding.tolist() for embedding in name_embeddings]
            yield pa.RecordBatch.from_arrays(
                [
                    pa.array(batch["id"], pa.int64()),
                    pa.array(batch["description"]),
                    pa.array(batch["name"]),
                    pa.array(batch["full_name"]),
                    pa.array(description_embeddings, pa.list_(pa.float32(), EMBEDDING_SIZE)),
                    pa.array(name_embeddings, pa.list_(pa.float32(), EMBEDDING_SIZE))
                ],
                ["id", "description", "name", "full_name", "description_embedding", "name_embedding"],
            )

    shutil.rmtree(REPO_DB_DIR)
    db.create_table("repo_info", make_batches(), schema=schema)
    con.close()
