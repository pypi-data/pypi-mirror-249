import os
from datetime import datetime, timedelta
from leptonai.client import Client, current
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

today = datetime.today()
client = Client("w3mgia27", "github-analytics-data", token=os.getenv("LEPTON_API_TOKEN"))

for i in tqdm(range(1000)):
    day = today - timedelta(days=i)
    date = day.strftime('%Y-%m-%d')
    result = client.fetch_archive(date=date)
    print(result)
