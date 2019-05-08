from pathlib import Path
import os
import sys
import requests

headers = {"content-type": "application/json"}
if len(sys.argv) != 3:
    print(f"usage: {sys.argv[0]} https://acct.cloudant.com/database ddocdir")
    exit(1)

baseurl, ddocdir = sys.argv[1:]
path = Path(ddocdir).resolve()
if not path.exists():
    print(f"Build dir '{path.name}' not found.")
    exit(1)

baseurl = baseurl.rstrip("/")

try:
    user = os.environ['COUCHDB_USER']
except IndexError:
    print(f"Expected a username in environment variable 'COUCHDB_USER'")
    exit(1)

try:
    passw = os.environ['COUCHDB_PW']
except IndexError:
    print(f"Expected a password in environment variable 'COUCHDB_PW'")
    exit(1)

session = requests.Session()
session.auth = (user, passw)

for filename in path.iterdir():
    ddoc, view = filename.stem.split("-")
    ddoc_url = f"{baseurl}/_design/{ddoc}"

    # Fetch existing
    params = {}
    existing_ddoc = session.get(ddoc_url)
    if existing_ddoc.status_code == 200:
        rev = existing_ddoc.json()["_rev"]
        params["rev"] = rev

    # Write new version, specifying rev if we have one.
    with open(filename, mode="r") as f:
        data = f.read()

    response = session.put(ddoc_url, data=data, headers=headers, params=params)
    response.raise_for_status()

    print(f"Uploaded new version of {ddoc_url}")
