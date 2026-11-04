import json
from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA\scripts")
from mapeamento_cursinho import MAPA_CURSINHO
from mapeamento_cursinho_pt2 import MAPA_CURSINHO_PT2

# Unir os dois mapas
MAPA_CURSINHO.update(MAPA_CURSINHO_PT2)

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
with open(BASE / "dados" / "banco_questoes.jsonl", encoding="utf-8") as f:
    rows = [json.loads(l) for l in f if l.strip()]

# Inverter: tema individual -> lista de capítulos
inverso = defaultdict(list)
for mat, caps in MAPA_CURSINHO.items():
    for cap, temas in caps.items():
        for t in temas:
            inverso[(mat, t.lower())].append(cap)

# Mapear cada questão para seus capítulos
questoes_por_cap = defaultdict(set)  # (mat, cap) -> set de qids
mapeamento_detalhado = defaultdict(list)  # (mat, cap) -> list de (ano, q, temas_originais)

for r in rows:
    mat = r["materia"]
    qid = f"{r['ano']} Q{r['q']}"
    caps_encontrados = set()
    for t in r.get("tema", []):
        chave = (mat, t.lower())
        if chave in inverso:
            for cap in inverso[chave]:
                caps_encontrados.add(cap)
    for cap in caps_encontrados:
        questoes_por_cap[(mat, cap)].add(qid)
        mapeamento_detalhado[(mat, cap)].append({
            "ano": r["ano"], "q": r["q"], "temas": r.get("tema", []),
            "tipo": r.get("tipo", ""), "gabarito": r.get("gabarito", ""),
        })

# Salvar contagem
saida = BASE / "metricas" / "frequencia_capitulos_cursinho.txt"
linhas = []
for mat in ["historia", "geografia", "filosofia", "sociologia"]:
    linhas.append(f"\n=== {mat.upper()} ===")
    itens = sorted(
        [(cap, qs) for (m, cap), qs in questoes_por_cap.items() if m == mat],
        key=lambda x: len(x[1]),
        reverse=True,
    )
    for cap, qs in itens:
        qs_str = ", ".join(sorted(qs))
        linhas.append(f"{len(qs):2d}x  {cap}  | {qs_str}")

saida.write_text("\n".join(linhas), encoding="utf-8")
print("Salvo em", saida)

# Salvar detalhado em JSON
detalhado = {}
for (mat, cap), qlist in mapeamento_detalhado.items():
    key = f"{mat}|{cap}"
    detalhado[key] = sorted(qlist, key=lambda x: (x["ano"], x["q"]))

saida_json = BASE / "dados" / "questoes_por_capitulo_cursinho.json"
with open(saida_json, "w", encoding="utf-8") as f:
    json.dump(detalhado, f, ensure_ascii=False, indent=2)
print("Salvo em", saida_json)
