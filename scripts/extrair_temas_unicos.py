import json
from collections import defaultdict
from pathlib import Path

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
with open(BASE / "dados" / "banco_questoes.jsonl", encoding="utf-8") as f:
    rows = [json.loads(l) for l in f if l.strip()]

por_materia = defaultdict(set)
for r in rows:
    for t in r.get("tema", []):
        por_materia[r["materia"]].add(t.lower())

for mat in ["historia", "geografia", "filosofia", "sociologia"]:
    temas = sorted(por_materia[mat])
    with open(BASE / "scripts" / f"temas_unicos_{mat}.txt", "w", encoding="utf-8") as f:
        for t in temas:
            f.write(t + "\n")
    print(f"{mat}: {len(temas)} temas unicos salvos")
