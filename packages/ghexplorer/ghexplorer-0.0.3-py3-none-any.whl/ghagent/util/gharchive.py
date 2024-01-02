import os
import gzip
from typing import List, Union
import requests
import duckdb
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from tqdm import tqdm
import pyarrow.parquet as pq
import pyarrow as pa
import glob

from ghagent.util.config import GHARCHIVE_DIR


def download_github_archive(date: str, output_dir: Union[str, Path]):
    """
    Download the github archive for a given date YYYY-MM-DD
    GHArchive website: https://www.gharchive.org/
    """
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)
    else:
        output_dir = output_dir
    urls = [f"https://data.gharchive.org/{date}-{hour}.json.gz" for hour in range(0, 24)]
    # NOTE: for dev/test purpose, only download/handle the first hour's data
    # urls = [f"https://data.gharchive.org/{date}-{hour}.json.gz" for hour in range(0, 1)]
    download_dir = Path.joinpath(output_dir, "download", date)
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # step 1: download the file form gharchive
    for url in urls:
        print(f"Downloading {url}")
        filename = Path.joinpath(download_dir, url.split("/")[-1])
        if filename.exists():
            print(f"File {filename} already exists, skipping download")
            continue
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

    # step 2: unzip the file to download_dir
    for file in download_dir.glob("*.gz"):
        print(f"Extracting file {file.name}")
        output_file_path = Path.joinpath(download_dir, file.name[:-3])
        if output_file_path.exists():
            print(f"File {output_file_path} already exists, skipping extraction")
            continue
        with gzip.open(file, 'rb') as f_in:
            with open(output_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    # step 3: aggregate the file to archive_dir as a single date.parquet
    print(f"Aggregating json files to {date}.parquet")
    parquet_file = Path.joinpath(output_dir, f"{date}.parquet")
    writer = None
    for file in tqdm(download_dir.glob("*.json"), total=len(glob.glob1(download_dir, "*.json")), desc=f"Aggregating json files to {date}.parquet"):
        query = f"SELECT id, type, actor, repo, created_at FROM read_json_auto('{file}', ignore_errors=true);" 
        try:
            partial_table = duckdb.sql(query).arrow()
            if writer is None:
                writer = pq.ParquetWriter(parquet_file, schema=pa.schema([
                    pa.field("id", pa.int64()),
                    pa.field("type", pa.utf8()),
                    pa.field("actor", pa.struct([
                            ("id", pa.int64()),
                            ("login", pa.utf8()),
                            ("display_login", pa.utf8()),
                            ("gravatar_id", pa.utf8()),
                            ("url", pa.utf8()),
                            ("avatar_url", pa.utf8()),
                        ])),
                    pa.field("repo", pa.struct([
                            ("id", pa.int64()),
                            ("name", pa.utf8()),
                            ("url", pa.utf8()),
                        ])),
                    pa.field("created_at", pa.timestamp('us')),
                ]))
            # Write the table to the Parquet file
            writer.write_table(partial_table)
        except Exception as e:
            print(f"Error aggregating json files: {e}")
            print(f"Query: {query}")
            # delete file
            parquet_file.unlink()
            raise(e)

    # step 4: delete the download_dir
    for file_path in download_dir.glob('*'):
        try:
            if file_path.is_file():
                print(f"Deleting file {file_path}")
                file_path.unlink()
        except Exception as e:
            print(f"Error deleting file: {e}")
    download_dir.rmdir()


def gen_date_list(start_date: str, end_date: str):
    """
    Generate a list of dates between start_date and end_date in the format YYYY-MM-DD
    """
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    date_list = []

    while start_date <= end_date:
        date_list.append(end_date.strftime('%Y-%m-%d'))
        end_date -= timedelta(days=1)
    return date_list

def get_all_event_dates(dir_path: Union[str, Path] = GHARCHIVE_DIR) -> List[str]:
    if isinstance(dir_path, str):
        dir_path = Path(dir_path)
    else:
        dir_path = dir_path
    dates = []
    for file in dir_path.glob("*.parquet"):
        dates.append(file.name.split(".")[0])
    dates.sort()
    return dates

def fetch_events(target_date_list: List[str], output_dir: Union[str, Path] = GHARCHIVE_DIR):
    """Fetch the repos for a given list of dates"""
    for target_date in tqdm(target_date_list):
        download_github_archive(target_date, output_dir)
        
def get_event_dates_to_download(target_start_date: str, target_end_date: str, output_dir: Union[str, Path] = GHARCHIVE_DIR):
    target_date_list = gen_date_list(target_start_date, target_end_date)
    existing_date_set = set(get_all_event_dates(output_dir))
    return [target_date for target_date in target_date_list if target_date not in existing_date_set]
