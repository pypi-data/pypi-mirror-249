import duckdb
import lancedb
import numpy as np
import gradio as gr
import pyarrow as pa
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List
from tqdm import tqdm

DATA_DIR = Path.joinpath(Path.home(), "data/github_archive_analytics")
GITHUB_EVENTS_DIR = Path.joinpath(DATA_DIR, "github_events")
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

def get_processed_repos() -> List[str]:
    db = lancedb.connect(LANCEDB_DIR)
    tables = db.table_names()
    suffix = "_related_users"
    repos = [table[:-(len(suffix))] for table in tables if table.endswith(suffix)]
    return repos

def search_relevant_related_repos(repo: str, query: str):
    if not repo:
        return None, 0, None, 0
    db = lancedb.connect(LANCEDB_DIR)
    repo_info = db.open_table("repo_info")
    related_repos = db.open_table(f"{repo}_related_repos").to_arrow()
    related_users = db.open_table(f"{repo}_related_users").to_arrow()
    if not query.strip():
        repo_info_arrow = repo_info.to_arrow()
    else:
        query_vector = MODEL.encode([query.strip()])[0]
        repo_info_arrow = repo_info.search(query_vector, "description_embedding").to_arrow()
    # step 1: find relevant related repos
    relevant_related_repos = duckdb.sql("SELECT r1.related_repo[:50] AS related_repo, r2.description[:50] AS description, string_agg(r1.common_stargazer)[:20] AS common_stargazers, count(r1.common_stargazer) AS common_stargazer_cnt FROM related_repos r1 JOIN repo_info_arrow r2 ON r1.related_repo = r2.full_name GROUP BY related_repo, description ORDER BY common_stargazer_cnt DESC LIMIT 1024;").fetch_arrow_table()
    # step 2: find relevant related users
    relevant_related_users = duckdb.sql("SELECT r1.related_user[:20] AS related_user, string_agg(r1.related_repo)[:50] as common_repos, count(r1.related_repo) AS common_repo_cnt FROM related_users r1 JOIN repo_info_arrow r2 ON r1.related_repo = r2.full_name GROUP BY related_user ORDER BY common_repo_cnt DESC LIMIT 1024;").fetch_arrow_table()
    return relevant_related_repos.to_pandas(), relevant_related_repos.num_rows, relevant_related_users.to_pandas(), relevant_related_users.num_rows

def launch():
    with gr.Blocks() as demo:
        gr.Markdown("Github-Analytics 🚀🚀🚀")

        with gr.Row():
            repo = gr.Dropdown(get_processed_repos(), label="Select a Repo")
            query = gr.Textbox(label="Search Query", placeholder="Search for a repo")
        search_button = gr.Button("Search")

        with gr.Accordion("Related Repos"):
            with gr.Row():
                relevant_related_repos_cnt = gr.Number(0, label="Number of relevant-related repos")
                gr.Label("🔥🔥🔥")
            relevant_related_repos = gr.DataFrame(headers=["Repo Name", "Description", "Common Stargazers", "Common Stargazer Count"], wrap=True)

        relevant_related_users_cnt = gr.Number(0, label="Number of relevant-related users")
        relevant_related_users = gr.DataFrame(headers=["User Name", "Common Stargazer Count", "Created At"])
        search_button.click(search_relevant_related_repos, inputs=[repo, query], outputs=[relevant_related_repos, relevant_related_repos_cnt, relevant_related_users, relevant_related_users_cnt])

    demo.launch()

if __name__ == "__main__":
    launch()
