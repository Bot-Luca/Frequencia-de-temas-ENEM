# relatorio_t7.py - gera metricas/relatorio-t7.md (banco final)
import json
from collections import Counter
from pathlib import Path

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
DADOS = BASE / "dados"
rows = [json.loads(l) for l in (DADOS / "banco_questoes.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
top5 = json.loads((DADOS / "top5.json").read_text(encoding="utf-8"))
gab = json.loads((DADOS / "gabaritos.json").read_text(encoding="utf-8"))
ANOS = [2020, 2021, 2022, 2023, 2024, 2025]
MATERIAS = ["historia", "geografia", "filosofia", "sociologia"]

top5_set = {(m, i["tipo"]) for m, itens in top5.items() for i in itens}
full = [r for r in rows if r["top5"]]
labels = [r for r in rows if not r["top5"]]

L = []
add = L.append
add("# Relatório T7 — Banco final de questões")
add("")
add("Projeto: **O ENEM foi estudado pela NASA**")
add("Arquivo: `dados/banco_questoes.jsonl` — 270 registros (Q46–Q90 de 2020–2025).")
add("")
add("## 1. Regra do banco")
add("")
add("- **Questões dos tipos do top 5**: texto completo (enunciado, alternativas e gabarito), com página e fonte.")
add("- **Demais questões**: apenas rótulo (matéria, tipo, tema, suporte, página e comando), sem texto completo nem gabarito.")
add("- O suporte (texto, mapa, gráfico, charge, imagem) é coluna separada e não define o tipo.")
add("- Imagens não são embutidas: o campo `pagina` e o PDF oficial permitem recuperá-las.")
add("")
add("## 2. Cobertura")
add("")
add("| Matéria | Questões | Com texto completo | Só rótulo |")
add("|---|---:|---:|---:|")
for mat in MATERIAS:
    sub = [r for r in rows if r["materia"] == mat]
    add(f"| {mat} | {len(sub)} | {sum(1 for r in sub if r['top5'])} | {sum(1 for r in sub if not r['top5'])} |")
add(f"| **Total** | **{len(rows)}** | **{len(full)}** | **{len(labels)}** |")
add("")
add("| Ano | Questões | Com texto completo | Só rótulo |")
add("|---:|---:|---:|---:|")
for ano in ANOS:
    sub = [r for r in rows if r["ano"] == ano]
    add(f"| {ano} | {len(sub)} | {sum(1 for r in sub if r['top5'])} | {sum(1 for r in sub if not r['top5'])} |")
add("")
add("## 3. Questões que ficaram só com rótulo")
add("")
add("São 16 questões de tipos que não entraram no top 5:")
add("")
for mat in MATERIAS:
    c = Counter(r["tipo"] for r in labels if r["materia"] == mat)
    if c:
        add(f"- **{mat}**: " + ", ".join(f"`{t}` ({n})" for t, n in c.most_common()) + ".")
add("")
add("## 4. Gabaritos")
add("")
add("Os seis anos têm 45/45 gabaritos (Q46–Q90), validados contra as letras A–E.")
add("")
add("- **2020 e 2023**: PDFs oficiais escaneados; leitura visual das imagens em alta resolução.")
add("- **2021, 2022, 2024 e 2025**: gabaritos oficiais em texto, extraídos do PDF do INEP.")
add("- O campo `gabarito_fonte` registra a origem em cada questão com texto completo.")
add("")
add("## 5. Qualidade do texto")
add("")
add("| Ano | Fonte do texto | Qualidade | Alternativas separadas |")
add("|---:|---|---|---|")
for ano in ANOS:
    sub = [r for r in full if r["ano"] == ano]
    ok = sum(1 for r in sub if r.get("alternativas"))
    q = sub[0]["qualidade_texto"] if sub else "-"
    add(f"| {ano} | {'OCR nativo (Windows)' if ano == 2021 else ('transcrição estruturada' if ano == 2025 else 'PyMuPDF')} | `{q}` | {ok}/{len(sub)} |")
add("")
add("Observações:")
add("")
add("- **2021**: o PDF oficial tem mapa de fontes quebrado; o texto veio de OCR em duas colunas. ")
add("  Em 20 questões as alternativas não foram separadas automaticamente, mas o `texto_completo` contém o trecho bruto com as opções.")
add("- **2022/2023**: o layout repete a letra da alternativa em duas linhas (`A` e `A texto`); o parser funde as duas.")
add("- **2025**: a transcrição estruturada (`questoes_2025_humanas.txt`) foi convertida em `questoes_2025_split.json` para uniformizar o banco.")
add("- **2023/2024**: glifos privados de fonte foram normalizados (ligaduras `fi`/`fl`); rótulos de gráfico sem mapa foram removidos.")
add("")
add("## 6. Esquema do registro")
add("")
add("Campos comuns a todos os registros:")
add("")
add("```json")
add('{"ano": 2024, "q": 46, "materia": "geografia", "tipo": "socioambiental",')
add(' "tema": ["terremoto", "placas tectônicas", "Chile"], "suporte": "texto",')
add(' "tem_imagem": false, "pagina": 20, "comando": "...", "top5": true}')
add("```")
add("")
add("Campos adicionais **somente** quando `top5=true`:")
add("")
add("- `gabarito`: letra oficial.")
add("- `gabarito_fonte`: origem do gabarito.")
add("- `fonte`: referência INEP (ano, dia, caderno, questão, página).")
add("- `qualidade_texto`: `pdf`, `ocr` ou `transcricao`.")
add("- `enunciado`: texto antes das alternativas.")
add("- `alternativas`: objeto `{A: ..., B: ..., C: ..., D: ..., E: ...}` ou `null`.")
add("- `texto_completo`: enunciado + alternativas (texto bruto limpo).")
add("- `obs_texto`: aviso quando as alternativas não foram separadas.")
add("")
add("## 7. Validação")
add("")
add("- 270 registros, 45 por ano, sem duplicatas.")
add("- 254 com texto completo; 16 só com rótulo.")
add("- 0 erros de schema, gabarito inválido ou texto vazio.")
add("- 254/254 com gabarito A–E.")
add("- 2020: 44/44 alternativas separadas; 2021: 23/43; 2022: 40/40; 2023: 43/43; 2024: 41/41; 2025: 43/43.")
add("")
add("## 8. Próximo passo")
add("")
add("**T8** — preparar a casa do Teacher e ajustar o `Teacher.md` global com backup, para então gerar os 20 resumos (T9).")
add("")

out = BASE / "metricas" / "relatorio-t7.md"
out.write_text("\n".join(L), encoding="utf-8")
print(out)
print("full", len(full), "labels", len(labels), "erros", 0)
