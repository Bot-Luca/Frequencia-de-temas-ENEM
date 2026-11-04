import json
from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA\scripts")
from mapeamento_por_palavra_chave import PALAVRA_CHAVE_PARA_CAPITULOS
from mapeamento_macrotema_capitulo import MAPA_MACROTEMA_CAPITULO

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
with open(BASE / "dados" / "banco_questoes.jsonl", encoding="utf-8") as f:
    rows = [json.loads(l) for l in f if l.strip()]

# Inverter: capitulo -> lista de macrotemas
inverso_cap_macro = defaultdict(list)
for mat, macros in MAPA_MACROTEMA_CAPITULO.items():
    for macro, caps in macros.items():
        for cap in caps:
            inverso_cap_macro[(mat, cap)].append(macro)

# Para cada questão: temas -> (substring match) -> capitulos -> macrotemas
questoes_por_macro = defaultdict(set)
detalhe = defaultdict(list)
questoes_sem_mapeamento = []

for r in rows:
    mat = r["materia"]
    qid = f"{r['ano']} Q{r['q']}"
    
    # Encontrar capitulos via substring match nos temas
    caps_da_questao = set()
    palavras = list(PALAVRA_CHAVE_PARA_CAPITULOS.get(mat, []))
    if mat == "historia":
        palavras += PALAVRA_CHAVE_PARA_CAPITULOS.get("historia_extras", [])
    for palavra_chave, caps in palavras:
        for t in r.get("tema", []):
            if palavra_chave in t.lower():
                for cap in caps:
                    caps_da_questao.add(cap)
    
    # Para cada capitulo, encontrar macrotemas
    macros_da_questao = set()
    for cap in caps_da_questao:
        chave = (mat, cap)
        if chave in inverso_cap_macro:
            for macro in inverso_cap_macro[chave]:
                macros_da_questao.add(macro)
    
    if not macros_da_questao:
        questoes_sem_mapeamento.append(qid)
    
    for macro in macros_da_questao:
        questoes_por_macro[(mat, macro)].add(qid)
        detalhe[(mat, macro)].append({
            "ano": r["ano"], "q": r["q"], "temas": r.get("tema", []),
            "tipo": r.get("tipo", ""), "gabarito": r.get("gabarito", ""),
            "capitulos": sorted(caps_da_questao),
        })

# Salvar contagem
saida = BASE / "metricas" / "frequencia_macrotema_capitulo_v4.txt"
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

# Salvar questoes sem mapeamento
saida_sem = BASE / "metricas" / "questoes_sem_mapeamento_v4.txt"
with open(saida_sem, "w", encoding="utf-8") as f:
    for qid in sorted(questoes_sem_mapeamento):
        f.write(qid + "\n")
print("Sem mapeamento:", len(questoes_sem_mapeamento), "->", saida_sem)

# Salvar detalhado em JSON
detalhado_json = {}
for (mat, macro), qlist in detalhe.items():
    key = f"{mat}|{macro}"
    detalhado_json[key] = sorted(qlist, key=lambda x: (x["ano"], x["q"]))

saida_json = BASE / "dados" / "questoes_por_macrotema_capitulo_v4.json"
with open(saida_json, "w", encoding="utf-8") as f:
    json.dump(detalhado_json, f, ensure_ascii=False, indent=2)
print("Salvo em", saida_json)

# Estatisticas
total_mapeado = len(rows) - len(questoes_sem_mapeamento)
print(f"Total mapeado: {total_mapeado}/{len(rows)}")
