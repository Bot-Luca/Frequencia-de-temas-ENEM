import json
from collections import defaultdict, Counter
from pathlib import Path
import sys

sys.path.insert(0, r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA\scripts")
from mapeamento_temas import MAPA

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
with open(BASE / "dados" / "banco_questoes.jsonl", encoding="utf-8") as f:
    rows = [json.loads(l) for l in f if l.strip()]

# Inverter mapa: tema individual -> macro-tema
inverso = {}
for mat, macro in MAPA.items():
    for macrotema, temas in macro.items():
        for t in temas:
            inverso[(mat, t.lower())] = macrotema

# Contar frequência por (matéria, macro-tema)
contagem = defaultdict(Counter)
questoes_por_macro = defaultdict(list)

for r in rows:
    mat = r["materia"]
    for t in r.get("tema", []):
        chave = (mat, t.lower())
        if chave in inverso:
            mt = inverso[chave]
            contagem[mat][mt] += 1
            questoes_por_macro[(mat, mt)].append(f"{r['ano']} Q{r['q']}")

# Salvar resultado
saida = BASE / "metricas" / "frequencia_macrotemas.txt"
linhas = []
for mat in ["historia", "geografia", "filosofia", "sociologia"]:
    linhas.append(f"\n=== {mat.upper()} ===")
    for mt, n in contagem[mat].most_common():
        qs = ", ".join(sorted(questoes_por_macro[(mat, mt)]))
        linhas.append(f"{n:2d}x  {mt}  | {qs}")

saida.write_text("\n".join(linhas), encoding="utf-8")
print("Salvo em", saida)
print("Total mapeado:", sum(sum(c.values()) for c in contagem.values()))
