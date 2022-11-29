import os
import requests
import json
import sqlite3
from datetime import date

from dotenv import load_dotenv
from pprint import pprint
 
load_dotenv()

def db_connect():
    con = sqlite3.connect("followers.db")
    with con:
        con.execute("CREATE TABLE IF NOT EXISTS followers (login PRIMARY KEY ON CONFLICT IGNORE, followed_at TIMESTAMP)")
    return con

def parse_link_next(header_link):
    for link in header_link.split(','):
      (url, rel) = link.split('; ')
      if rel == 'rel="next"':
          return url[1:-1]

token = os.getenv('GITHUB_ACCESS_TOKEN')
user = os.getenv('GITHUB_USER')
api_root = "https://api.github.com"

headers = { 
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}"
}

link = f"{api_root}/users/{user}/followers"
res = []
i = 1
while link is not None:
    print(f"Fetching follower data for {user} (page {i})...")
    fetch = requests.get(
        link, headers=headers
    )
    res += json.loads(fetch.content)
    if 'Link' in fetch.headers:
        link = parse_link_next(fetch.headers['Link'])
    else:
        link = None
    i += 1

con = db_connect()

datestamp = date.today().strftime("%Y-%m-%d") 
print("Saving follower data to database...")
with con:
    con.executemany(
        "INSERT INTO followers (login, followed_at) VALUES (?, ?)",
        [ (follower['login'], datestamp) for follower in res ]
    )

print("Update complete")

import plotext as plt

def format_date(date):
    return date.replace("T", " ").replace("Z", "")

with con:
    res = con.execute("SELECT followed_at, COUNT(login) FROM followers GROUP BY followed_at")

data_points = []
for row in res.fetchall():
    data_points.append([ format_date(row[0]), row[1] ])
plt.date_form(input_form='Y-m-d', output_form='d/m/Y')

start = plt.string_to_datetime(format_date(data_points[0][0]))
end = plt.today_datetime()
data = [ [r[1]] for r in data_points ]
dates = [ r[0] for r in data_points ]

plt.plot(dates, [ d[0] for d in data ])
plt.title("Followers")
plt.xlabel("Date")
plt.ylabel("Followers")
plt.show()
