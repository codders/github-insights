import os
import requests
import json
import sqlite3

from dotenv import load_dotenv
from pprint import pprint
 
load_dotenv()

def db_connect():
    con = sqlite3.connect("traffic.db")
    with con:
        con.execute("CREATE TABLE IF NOT EXISTS views (timestamp TIMESTAMP PRIMARY KEY ON CONFLICT REPLACE, views INTEGER, uniques INTEGER)")
    return con 

token = os.getenv('GITHUB_ACCESS_TOKEN')
repo = os.getenv('GITHUB_REPO')
api_root = "https://api.github.com"

headers = { 
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}"
}

print(f"Fetching repo traffic data for {repo}...")
res = json.loads(
    requests.get(
        f"{api_root}/repos/{repo}/traffic/views", headers=headers
    ).content
)

con = db_connect()

print("Saving traffic data to database...")
with con:
    con.executemany(
        "INSERT INTO views (timestamp, views, uniques) VALUES (?, ?, ?)",
        [ (view['timestamp'], view['count'], view['uniques']) for view in res['views'] ]
    )

print("Update complete")

