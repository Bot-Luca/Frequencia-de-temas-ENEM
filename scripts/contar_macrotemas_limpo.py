import json
from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA\scripts")
from mapeamento_temas import MAPA

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
with open(BASE / "dados" / "banco_questoes.jsonl", encoding="utf-8") as f:
    rows = [json.loads(l) for l in f if l.strip()]

inverso = {}
for mat, macro in MAPA.items():
    for macrotema, temas in macro.items():
        for t in temas:
            inverso[(mat, t.lower())] = macrotema

# Usar set para deduplicar questões por macro-tema
questoes_por_macro = defaultdict(set)

for r in rows:
    mat = r["materia"]
    qid = f"{r['ano']} Q{r['q']}"
    macrotemas_da_questao = set()
    for t in r.get("tema", []):
        chave = (mat, t.lower())
        if chave in inverso:
            macrotemas_da_questao.add(inverso[chave])
    for mt in macrotemas_da_questao:
        questoes_por_macro[(mat, mt)].add(qid)

# Contar e salvar
saida = BASE / "metricas" / "frequencia_macrotemas_limpo.txt"
linhas = []
for mat in ["historia", "geografia", "filosofia", "sociologia"]:
    linhas.append(f"\n=== {mat.upper()} ===")
    # Ordenar por contagem decrescente
    itens = sorted(
        [(mt, qs) for (m, mt), qs in questoes_por_macro.items() if m == mat],
        key=lambda x: len(x[1]),
        reverse=True,
    )
    for mt, qs in itens:
        qs_str = ", ".join(sorted(qs))
        linhas.append(f"{len(qs):2d}x  {mt}  | {qs_str}")

saida.write_text("\n".join(linhas), encoding="utf-8")
print("Salvo em", saida)
