from fastapi import FastAPI
import psycopg2
import os
import requests
import base64
import gzip

app = FastAPI()

def fetch_sql_dump():
    access_token = os.getenv("ACCESS_TOKEN")

    url = f"https://hackattic.com/challenges/backup_restore/problem?access_token={access_token}"
    response = requests.get(url)
    data = response.json()

    dump_path = "/test-task-data/dump.sql.gz"
    extracted_path = "/test-task-data/dump.sql"

    with open(dump_path, "wb") as f:
        f.write(base64.b64decode(data["dump"]))

    with gzip.open(dump_path, "rb") as f_in:
        with open(extracted_path, "wb") as f_out:
            f_out.write(f_in.read())

    return extracted_path

def get_alive_ssns():
    conn = psycopg2.connect(
        dbname="test_db",
        user="postgres",
        password="secret",
        host="db",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT ssn FROM criminal_records WHERE status = 'alive';")
    ssns = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return ssns

@app.get("/fetch-dump")
def fetch_dump():
    dump_file = fetch_sql_dump()
    return {
        "dump_file": dump_file
    }

@app.get("/fetch-alive-ssns")
def alive_ssns():
    ssns = get_alive_ssns()
    return {
        "alive_ssns": ssns
    }
