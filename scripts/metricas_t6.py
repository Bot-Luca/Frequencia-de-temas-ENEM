# metricas_t6.py - contagens e matriz tipo x ano da classificacao 2020-2025.
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
DADOS = BASE / "dados"
ANOS = [2020, 2021, 2022, 2023, 2024, 2025]

rows = []
for ano in ANOS:
    p = DADOS / f"classificacao_{ano}.jsonl"
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            rows.append(r)

print("=== TOTAL POR ANO ===")
for ano in ANOS:
    sub = [r for r in rows if r["ano"] == ano]
    print(ano, len(sub), dict(Counter(r["materia"] for r in sub)))

print("\n=== PAGINAS NULAS / SUPORTE ===")
for ano in ANOS:
    sub = [r for r in rows if r["ano"] == ano]
    nulos = [r["q"] for r in sub if r["pagina"] is None]
    print(ano, "paginas_nulas=", nulos, "suporte=", dict(Counter(r["suporte"] for r in sub)))

print("\n=== MATERIA x TIPO (total 2020-2025) ===")
for mat in ["historia", "geografia", "filosofia", "sociologia", "interdisciplinar"]:
    c = Counter(r["tipo"] for r in rows if r["materia"] == mat)
    if not c:
        continue
    print(f"\n[{mat}] n={sum(c.values())}")
    for tipo, n in c.most_common():
        anos = sorted({r["ano"] for r in rows if r["materia"] == mat and r["tipo"] == tipo})
        print(f"  {tipo:<28} {n:>3}  anos={anos} ({len(anos)})")

print("\n=== MATRIZ TIPO x ANO ===")
tipos = sorted({(r["materia"], r["tipo"]) for r in rows})
matriz = defaultdict(lambda: defaultdict(int))
for r in rows:
    matriz[(r["materia"], r["tipo"])][r["ano"]] += 1
print("materia|tipo|" + "|".join(str(a) for a in ANOS) + "|total|anos")
for mat, tipo in tipos:
    vals = [matriz[(mat, tipo)][a] for a in ANOS]
    anos = sum(1 for v in vals if v)
    print(f"{mat}|{tipo}|" + "|".join(str(v) for v in vals) + f"|{sum(vals)}|{anos}")

print("\n=== TIPOS COM >=3 ANOS ===")
for mat in ["historia", "geografia", "filosofia", "sociologia"]:
    eleg = []
    for tipo in sorted({r["tipo"] for r in rows if r["materia"] == mat}):
        anos = {r["ano"] for r in rows if r["materia"] == mat and r["tipo"] == tipo}
        if len(anos) >= 3:
            eleg.append((tipo, len(anos), sum(1 for r in rows if r["materia"] == mat and r["tipo"] == tipo)))
    print(mat, eleg)

print("\n=== OUTRO ===")
for ano in ANOS:
    sub = [r for r in rows if r["ano"] == ano]
    n = sum(1 for r in sub if r["tipo"] == "outro")
    print(ano, n, f"({100*n/len(sub):.1f}%)")
