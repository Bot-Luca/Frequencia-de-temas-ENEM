import json
from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA\scripts")
from mapeamento_por_palavra_chave import PALAVRA_CHAVE_PARA_CAPITULOS

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
with open(BASE / "dados" / "banco_questoes.jsonl", encoding="utf-8") as f:
    rows = [json.loads(l) for l in f if l.strip()]

mat = "historia"
sem_mapeamento = []
palavras = list(PALAVRA_CHAVE_PARA_CAPITULOS.get(mat, []))
palavras += PALAVRA_CHAVE_PARA_CAPITULOS.get("historia_extras", [])

for r in rows:
    if r["materia"] != mat:
        continue
    qid = f"{r['ano']} Q{r['q']}"
    caps_da_questao = set()
    for palavra_chave, caps in palavras:
        for t in r.get("tema", []):
            if palavra_chave in t.lower():
                for cap in caps:
                    caps_da_questao.add(cap)
    if not caps_da_questao:
        sem_mapeamento.append((qid, r.get("tema", [])))

print(f"Total sem mapeamento: {len(sem_mapeamento)}")
for qid, temas in sem_mapeamento:
    print(qid, "|", ", ".join(temas))
