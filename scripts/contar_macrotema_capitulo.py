import json
from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA\scripts")

from mapeamento_cursinho import MAPA_CURSINHO
from mapeamento_cursinho_pt2 import MAPA_CURSINHO_PT2
from mapeamento_macrotema_capitulo import MAPA_MACROTEMA_CAPITULO

# Unir mapas tema->capitulo
MAPA_TEMA_CAPITULO = {}
MAPA_TEMA_CAPITULO.update(MAPA_CURSINHO)
MAPA_TEMA_CAPITULO.update(MAPA_CURSINHO_PT2)

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
with open(BASE / "dados" / "banco_questoes.jsonl", encoding="utf-8") as f:
    rows = [json.loads(l) for l in f if l.strip()]

# Inverter: tema individual -> lista de capitulos
inverso_tema_cap = defaultdict(list)
for mat, caps in MAPA_TEMA_CAPITULO.items():
    for cap, temas in caps.items():
        for t in temas:
            inverso_tema_cap[(mat, t.lower())].append(cap)

# Inverter: capitulo -> lista de macrotemas
inverso_cap_macro = defaultdict(list)
for mat, macros in MAPA_MACROTEMA_CAPITULO.items():
    for macro, caps in macros.items():
        for cap in caps:
            inverso_cap_macro[(mat, cap)].append(macro)

# Para cada questão: temas -> capitulos -> macrotemas
questoes_por_macro = defaultdict(set)  # (mat, macro) -> set de qids
detalhe = defaultdict(list)  # (mat, macro) -> list de dicts

for r in rows:
    mat = r["materia"]
    qid = f"{r['ano']} Q{r['q']}"
    
    # Encontrar capitulos da questão
    caps_da_questao = set()
    for t in r.get("tema", []):
        chave = (mat, t.lower())
        if chave in inverso_tema_cap:
            for cap in inverso_tema_cap[chave]:
                caps_da_questao.add(cap)
    
    # Para cada capitulo, encontrar macrotemas
    macros_da_questao = set()
    for cap in caps_da_questao:
        chave = (mat, cap)
        if chave in inverso_cap_macro:
            for macro in inverso_cap_macro[chave]:
                macros_da_questao.add(macro)
    
    for macro in macros_da_questao:
        questoes_por_macro[(mat, macro)].add(qid)
        detalhe[(mat, macro)].append({
            "ano": r["ano"], "q": r["q"], "temas": r.get("tema", []),
            "tipo": r.get("tipo", ""), "gabarito": r.get("gabarito", ""),
            "capitulos": sorted(caps_da_questao),
        })

# Salvar contagem
saida = BASE / "metricas" / "frequencia_macrotema_capitulo.txt"
linhas = []
for mat in ["historia", "geografia", "filosofia", "sociologia"]:
    linhas.append(f"\n=== {mat.upper()} ===")
    itens = sorted(
        [(macro, qs) for (m, macro), qs in questoes_por_macro.items() if m == mat],
        key=lambda x: len(x[1]),
        reverse=True,
    )
    for macro, qs in itens:
        qs_str = ", ".join(sorted(qs))
        linhas.append(f"{len(qs):2d}x  {macro}  | {qs_str}")

saida.write_text("\n".join(linhas), encoding="utf-8")
print("Salvo em", saida)

# Salvar detalhado em JSON
detalhado_json = {}
for (mat, macro), qlist in detalhe.items():
    key = f"{mat}|{macro}"
    detalhado_json[key] = sorted(qlist, key=lambda x: (x["ano"], x["q"]))

saida_json = BASE / "dados" / "questoes_por_macrotema_capitulo.json"
with open(saida_json, "w", encoding="utf-8") as f:
    json.dump(detalhado_json, f, ensure_ascii=False, indent=2)
print("Salvo em", saida_json)

# Estatisticas de cobertura
total_mapeado = sum(len(s) for s in questoes_por_macro.values())
print(f"\nTotal de questoes mapeadas (contando multiplos macrotemas): {total_mapeado}")
print("Total de questoes no banco:", len(rows))
