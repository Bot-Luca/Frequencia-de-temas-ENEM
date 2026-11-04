# validar_banco.py - valida o banco final e mostra amostras.
import json
from collections import Counter
from pathlib import Path

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
DADOS = BASE / "dados"
rows = [json.loads(l) for l in (DADOS / "banco_questoes.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
top5 = json.loads((DADOS / "top5.json").read_text(encoding="utf-8"))
top5_set = {(m, i["tipo"]) for m, itens in top5.items() for i in itens}

print("linhas:", len(rows))
print("top5:", sum(r["top5"] for r in rows), "rotulo:", sum(not r["top5"] for r in rows))
print("por ano:", dict(Counter(r["ano"] for r in rows)))
print("por materia:", dict(Counter(r["materia"] for r in rows)))

erros = []
for r in rows:
    if r["top5"] != ((r["materia"], r["tipo"]) in top5_set):
        erros.append(f"{r['ano']} Q{r['q']}: top5 inconsistente")
    if r["top5"]:
        for campo in ["gabarito", "texto_completo", "enunciado", "fonte", "qualidade_texto"]:
            if campo not in r:
                erros.append(f"{r['ano']} Q{r['q']}: falta {campo}")
        if r.get("gabarito") not in list("ABCDE"):
            erros.append(f"{r['ano']} Q{r['q']}: gabarito invalido {r.get('gabarito')}")
        if not r.get("texto_completo"):
            erros.append(f"{r['ano']} Q{r['q']}: texto vazio")
    else:
        if "texto_completo" in r or "gabarito" in r:
            erros.append(f"{r['ano']} Q{r['q']}: rotulo com texto/gabarito")
    if not r.get("comando"):
        erros.append(f"{r['ano']} Q{r['q']}: comando vazio")

print("erros:", len(erros))
for e in erros[:20]:
    print(" ", e)

print("\nalternativas parseadas por ano:")
for ano in range(2020, 2026):
    sub = [r for r in rows if r["ano"] == ano and r["top5"]]
    ok = sum(1 for r in sub if r.get("alternativas"))
    print(ano, f"{ok}/{len(sub)}")

print("\namostra 2024 Q46:")
r = next(x for x in rows if x["ano"] == 2024 and x["q"] == 46)
print("tipo:", r["tipo"], "gab:", r["gabarito"], "alt:", r["alternativas"])
print("enunciado:", r["enunciado"][:300].replace("\n", " "))
print("texto:", r["texto_completo"][-500:].replace("\n", " "))

print("\namostra 2021 Q46 (OCR):")
r = next(x for x in rows if x["ano"] == 2021 and x["q"] == 46)
print("tipo:", r["tipo"], "gab:", r["gabarito"], "alt:", r["alternativas"])
print("texto:", r["texto_completo"][-500:].replace("\n", " "))
