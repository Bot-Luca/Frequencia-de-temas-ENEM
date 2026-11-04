import sqlite3
from pathlib import Path

db = Path(r"C:\Users\Luca\.local\share\opencode\opencode.db")
con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
q = """
select session_id, count(*), min(time_created), max(time_updated)
from session_message
where data like '%ENEM%' or data like '%NASA%' or data like '%classificacao%'
group by session_id
"""
for r in con.execute(q):
    print(r)
