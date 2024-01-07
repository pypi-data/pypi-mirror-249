# lep photon create -n github-analytics-data -m lepton_data.py
# lep photon push -n github-analytics-data
# lep deployment remove -n github-analytics-data
# lep photon run -n github-analytics-data -dn github-analytics-data --mount /github-analytics/data:/mnt/data

from leptonai.photon import Photon
import os
import requests
import shutil
import duckdb
import gzip
from pathlib import Path

class GithubAnalyticsData(Photon):
    requirement_dependency = ["duckdb", "lancedb"]

    def init(self):
        self.counter = 0
        self.data_dir = Path("/mnt/data")

    def _fetch_archive(self, date: str):
        # date: 2021-01-01
        urls = [f"https://data.gharchive.org/{date}-{hour}.json.gz" for hour in range(0, 24)]
        download_dir = Path.joinpath(self.data_dir, "download", date)
        archive_dir = Path.joinpath(self.data_dir, "github-archive")
        os.makedirs(download_dir, exist_ok=True)
        os.makedirs(archive_dir, exist_ok=True)
        # step 1: download the file form gharchive
        for url in urls:
            print(f"Downloading {url}")
            filename = Path.joinpath(download_dir, url.split("/")[-1])
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        # step 2: unzip the file to download_dir
        for file in download_dir.glob("*.gz"):
            output_file_path = Path.joinpath(download_dir, file.name[:-3])
            with gzip.open(file, 'rb') as f_in:
                with open(output_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        # step 3: aggregate the file to archive_dir as a single date.parquet
        print(f"Aggregating json files to {date}.parquet")
        parquet_file = Path.joinpath(archive_dir, f"{date}.parquet")
        query = f"COPY (SELECT * FROM read_json_auto('{download_dir}/*.json', ignore_errors=true)) TO '{parquet_file}';"
        duckdb.sql(query)
        # step 4: delete the download_dir
        for file_path in download_dir.glob('*'):
            try:
                if file_path.is_file():
                    print(f"Deleting file {file_path}")
                    file_path.unlink()
            except Exception as e:
                print(f"Error deleting file: {e}")
        download_dir.rmdir()

    @Photon.handler()
    def fetch_archive(self, date: str) -> bool:
        self.add_background_task(self._fetch_archive, date)
        return True
