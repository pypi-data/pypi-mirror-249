import modal
import datetime
import requests
import shutil
import boto3
import gzip
import duckdb
from modal import Image
from tqdm import tqdm

stub = modal.Stub("extract_watch_events")
image = Image.debian_slim().apt_install("wget").pip_install("pandas", "numpy", "requests", "tqdm", "boto3", "duckdb")
archive_volume = modal.Volume.new()
archive_path = "/vol/github-archives"

@stub.function(volumes={archive_path: archive_volume}, image=image)
def extract_watch_events(start_date, end_date):
    s3 = boto3.client(
        service_name ="s3",
        endpoint_url = 'https://a199e11f0d1168b4a64525b6ca1ee728.r2.cloudflarestorage.com',
        aws_access_key_id = '3a2f8c198906f447a7a059179280d4ff',
        aws_secret_access_key = 'f5d96367db6d13b4eccb943d8614ca209d74cfa946a19ccd91dfebf2449dfdeb',
        region_name="auto", # Must be one of: wnam, enam, weur, eeur, apac, auto
    )
    con = duckdb.connect()
    all_events = []
    # create list of date strings from start_date to end_date
    date_list = [start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    date_strings = [date.strftime("%Y-%m-%d") for date in date_list]
    for date_string in tqdm(date_strings):
        for i in range(0, 24):
            # download the file form gharchive
            url = f"https://data.gharchive.org/{date_string}-{i}.json.gz"
            filename = f"{archive_path}/{date_string}-{i}.json.gz"
            jsonfile = f"{archive_path}/{date_string}-{i}.json"
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            # extract the .gz file
            with gzip.open(filename, 'rb') as f_in:
                with open(jsonfile, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            # extract the watch events
            events = con.execute(f"SELECT actor.login, actor.url, repo.name, repo.url, created_at from read_json_auto('{jsonfile}', ignore_errors=true) where type='WatchEvent';").fetchall()
            all_events.extend(events)
    con.close()
    return True

@stub.local_entrypoint()
def main():
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2023, 9, 26)
    extract_watch_events.remote(start_date, end_date)
    # dates = [
    #     (datetime.date(2022, 1, 1), datetime.date(2022, 12, 31)),
    #     (datetime.date(2023, 1, 1), datetime.date(2023, 9, 26))
    # ]
    # list(download_github_archives.starmap(dates))
