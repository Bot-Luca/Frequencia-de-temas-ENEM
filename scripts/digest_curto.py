# digest_curto.py - resumo compacto por questao para classificacao.
# uso: python digest_curto.py ANO [inicio fim] [--compacto]
import json
import re
import sys
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
compacto = "--compacto" in sys.argv
ano = int(args[0])
ini = int(args[1]) if len(args) > 1 else 46
fim = int(args[2]) if len(args) > 2 else 90

base = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
dados = json.loads((base / "dados" / f"questoes_{ano}_split.json").read_text(encoding="utf-8"))


def limpar(t: str) -> str:
    t = t.replace("\ufb01", "fi").replace("\ufb02", "fl")
    t = re.sub(r"===+ PAGINA \d+.*?===+", " ", t)
    t = re.sub(r"PAGINA \d+ \(COLUNA [A-Z]+\)", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def comando(t: str) -> str:
    linhas = t.splitlines()
    corte = len(linhas)
    achou = []
    for i, ln in enumerate(linhas):
        m = re.match(r"^\s*([A-E])\s+\S", ln)
        if m:
            achou.append((i, m.group(1)))
    for k in range(len(achou) - 3):
        letras = [b[1] for b in achou[k:k + 5]]
        if letras[:4] == ["A", "B", "C", "D"]:
            corte = achou[k][0]
            break
    stem = " ".join(linhas[:corte]).strip()
    if not stem:
        stem = " ".join(linhas).strip()
    return limpar(stem)


for q in range(ini, fim + 1):
    t = dados.get(str(q), "")
    if not t:
        print(f"Q{q} VAZIA")
        continue
    c = comando(t)
    apoio = limpar(t)[:60]
    cmd = c[-170:] if len(c) > 170 else c
    if compacto:
        print(f"Q{q}|{apoio}|{cmd}")
    else:
        print(f"Q{q} | APOIO: {apoio}")
        print(f"     CMD: {cmd}")
