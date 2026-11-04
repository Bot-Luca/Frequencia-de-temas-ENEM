# digest_ano.py - mostra um resumo legivel das questoes de um ano para classificacao.
import json
import re
import sys
from pathlib import Path

ano = int(sys.argv[1])
base = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
dados = json.loads((base / "dados" / f"questoes_{ano}_split.json").read_text(encoding="utf-8"))

for q in range(46, 91):
    t = dados.get(str(q), "")
    t = re.sub(r"\s+", " ", t)
    # tenta achar inicio das alternativas
    m = re.search(r"(?:^|\s)([A-E])\s{1,}(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])", t)
    corte = len(t)
    if m and m.start() > 150:
        corte = m.start()
    comando = t[max(0, corte - 420):corte].strip()
    inicio = t[:260].strip()
    print(f"--- Q{q} ---")
    print("INICIO:", inicio)
    print("COMANDO:", comando)
