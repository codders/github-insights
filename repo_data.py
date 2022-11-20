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

import plotext as plt

def format_date(date):
    return date.replace("T", " ").replace("Z", "")

with con:
    res = con.execute("SELECT timestamp, views, uniques FROM views")

data_points = []
for row in res.fetchall():
    data_points.append([ format_date(row[0]), row[1], row[2] ])
plt.date_form(input_form='Y-m-d H:M:S', output_form='d/m/Y')

start = plt.string_to_datetime(format_date(data_points[0][0]))
end = plt.today_datetime()
data = [ [r[1], r[2]] for r in data_points ]
dates = [ r[0] for r in data_points ]

plt.plot(dates, [ d[0] for d in data ])
plt.plot(dates, [ d[1] for d in data ])
plt.title("Traffic")
plt.xlabel("Date")
plt.ylabel("Impressions")
plt.show()

