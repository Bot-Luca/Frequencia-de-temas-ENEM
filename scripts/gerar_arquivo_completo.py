import json
from pathlib import Path

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")

# Carregar o mapeamento detalhado v4
with open(BASE / "dados" / "questoes_por_macrotema_capitulo_v4.json", encoding="utf-8") as f:
    dados = json.load(f)

# Carregar o banco para pegar tipo, gabarito e comando
with open(BASE / "dados" / "banco_questoes.jsonl", encoding="utf-8") as f:
    banco = {}
    for l in f:
        if l.strip():
            r = json.loads(l)
            banco[(r["materia"], f"{r['ano']} Q{r['q']}")] = r

# Gerar arquivo texto completo
linhas = []
linhas.append("# QUESTOES DO ENEM POR CAPITULO DO CURSINHO")
linhas.append("")
linhas.append("Macro-temas aprovados mapeados para os capítulos do cursinho.")
linhas.append("Uma questão pode aparecer em múltiplos macro-temas.")
linhas.append("")

for mat in ["historia", "geografia", "filosofia", "sociologia"]:
    linhas.append(f"\n{'='*60}")
    linhas.append(f"# {mat.upper()}")
    linhas.append(f"{'='*60}")
    
    # Separar por macro-tema
    macro_itens = []
    for key, qlist in dados.items():
        if key.startswith(mat + "|"):
            macro_name = key.split("|", 1)[1]
            macro_itens.append((macro_name, qlist))
    
    # Ordenar por quantidade decrescente
    macro_itens.sort(key=lambda x: len(x[1]), reverse=True)
    
    for macro_name, qlist in macro_itens:
        qlist_sorted = sorted(qlist, key=lambda x: (x["ano"], x["q"]))
        linhas.append(f"\n## {macro_name} ({len(qlist_sorted)} questões)")
        linhas.append("-" * 50)
        for item in qlist_sorted:
            ano = item["ano"]
            q = item["q"]
            chave = (mat, f"{ano} Q{q}")
            r = banco.get(chave, {})
            tipo = r.get("tipo", "-")
            gabarito = r.get("gabarito", "-")
            temas = ", ".join(item.get("temas", []))
            caps = ", ".join(item.get("capitulos", []))
            linhas.append(f"  {ano} Q{q:02d} | tipo={tipo:<28} | gab={gabarito} | temas: {temas}")
            linhas.append(f"      cap: {caps}")

out = BASE / "metricas" / "questoes_por_capitulo_completo.txt"
out.write_text("\n".join(linhas), encoding="utf-8")
print("Salvo em", out)
print("Total de linhas:", len(linhas))
