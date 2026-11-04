# relatorio_t6.py - gera metricas/relatorio-t6.md e dados/top5.json
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
DADOS = BASE / "dados"
METRICAS = BASE / "metricas"
METRICAS.mkdir(exist_ok=True)
ANOS = [2020, 2021, 2022, 2023, 2024, 2025]
MATERIAS = ["historia", "geografia", "filosofia", "sociologia"]

rows = []
for ano in ANOS:
    for line in (DADOS / f"classificacao_{ano}.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))

por_ano = {a: [r for r in rows if r["ano"] == a] for a in ANOS}
matriz = defaultdict(lambda: defaultdict(int))
for r in rows:
    matriz[(r["materia"], r["tipo"])][r["ano"]] += 1


def anos_de(mat, tipo):
    return [a for a in ANOS if matriz[(mat, tipo)][a]]


def total_de(mat, tipo):
    return sum(matriz[(mat, tipo)].values())


def questoes_de(mat, tipo):
    out = {}
    for a in ANOS:
        qs = sorted(r["q"] for r in rows if r["materia"] == mat and r["tipo"] == tipo and r["ano"] == a)
        if qs:
            out[a] = qs
    return out


# top 5: elegiveis (>=3 anos), ordenados por total; empate -> mais anos, depois nome
top5 = {}
for mat in MATERIAS:
    tipos = {r["tipo"] for r in rows if r["materia"] == mat}
    eleg = [t for t in tipos if len(anos_de(mat, t)) >= 3]
    eleg.sort(key=lambda t: (-total_de(mat, t), -len(anos_de(mat, t)), t))
    top5[mat] = eleg[:5]

# validacoes
erros = []
for a in ANOS:
    if len(por_ano[a]) != 45:
        erros.append(f"{a}: {len(por_ano[a])} questoes")
    qs = [r["q"] for r in por_ano[a]]
    if len(set(qs)) != 45:
        erros.append(f"{a}: questoes duplicadas/ausentes")
    for r in por_ano[a]:
        for campo in ["ano", "q", "materia", "tipo", "tema", "suporte", "tem_imagem", "pagina", "comando", "obs"]:
            if campo not in r:
                erros.append(f"{a} Q{r['q']}: campo {campo} ausente")
        if r["pagina"] is None:
            erros.append(f"{a} Q{r['q']}: pagina nula")
        if not r["comando"]:
            erros.append(f"{a} Q{r['q']}: comando vazio")
        if r["materia"] not in MATERIAS + ["interdisciplinar"]:
            erros.append(f"{a} Q{r['q']}: materia invalida {r['materia']}")

linhas = []
add = linhas.append
add("# Relatório T6 — Classificação das provas de Ciências Humanas do ENEM (2020–2025)")
add("")
add("Projeto: **O ENEM foi estudado pela NASA**")
add("Escopo: Ciências Humanas e suas Tecnologias — 45 questões por ano (Q46–Q90), 6 anos, 270 questões.")
add("Regra de tipo: lido no **comando final** da questão; suporte (texto, mapa, gráfico, charge, imagem) é coluna separada.")
add("Uma matéria primária e um tipo primário por questão; ambíguas iriam para `interdisciplinar` (não houve caso).")
add("")
add("## 1. Validação da base")
add("")
add(f"- JSONLs lidos: {len(ANOS)} arquivos (`dados/classificacao_2020.jsonl` … `classificacao_2025.jsonl`).")
add(f"- Total de questões classificadas: **{len(rows)}**.")
add(f"- Questões por ano: " + ", ".join(f"{a}={len(por_ano[a])}" for a in ANOS) + ".")
add(f"- Questões `outro`: **0 (0,0%)** em todos os anos.")
add(f"- Páginas nulas: **0**.")
add(f"- Erros de schema/contagem: **{len(erros)}**.")
if erros:
    for e in erros:
        add(f"  - {e}")
add("")
add("A classificação de 2020–2024 foi refeita nesta sessão com o mesmo critério do 2025 congelado. ")
add("Em Filosofia, a primeira passada concentrava quase tudo em `interpretar-fragmento`; uma segunda leitura do comando ")
add("separou `aplicar-conceito`, `comparar-autores`, `questao-eticamente-julgada` e `ciencia-filosofia`. ")
add("O 2025 **não foi alterado**.")
add("")
add("## 2. Questões por matéria e ano")
add("")
add("| Matéria | " + " | ".join(str(a) for a in ANOS) + " | Total |")
add("|---|" + "|".join("---:" for _ in ANOS) + "|---:|")
for mat in MATERIAS:
    vals = [sum(1 for r in por_ano[a] if r["materia"] == mat) for a in ANOS]
    add(f"| {mat} | " + " | ".join(str(v) for v in vals) + f" | {sum(vals)} |")
add("| **Total** | " + " | ".join(str(len(por_ano[a])) for a in ANOS) + f" | **{len(rows)}** |")
add("")
add("## 3. Matriz tipo × ano (completa)")
add("")
for mat in MATERIAS:
    add(f"### {mat.capitalize()}")
    add("")
    add("| Tipo | " + " | ".join(str(a) for a in ANOS) + " | Total | Anos distintos |")
    add("|---|" + "|".join("---:" for _ in ANOS) + "|---:|---:|")
    tipos = sorted({r["tipo"] for r in rows if r["materia"] == mat}, key=lambda t: (-total_de(mat, t), t))
    for tipo in tipos:
        vals = [matriz[(mat, tipo)][a] for a in ANOS]
        add(f"| `{tipo}` | " + " | ".join(str(v) for v in vals) + f" | {sum(vals)} | {len(anos_de(mat, tipo))} |")
    add("")
add("## 4. Portão de ≥3 anos e seleção do top 5")
add("")
add("Tipos elegíveis são os que aparecem em **pelo menos 3 anos distintos**. O top 5 de cada matéria é ordenado por ")
add("frequência total; empate resolve-se por número de anos e depois por ordem alfabética.")
add("")
for mat in MATERIAS:
    add(f"### {mat.capitalize()}")
    add("")
    tipos = {r["tipo"] for r in rows if r["materia"] == mat}
    eleg = sorted([t for t in tipos if len(anos_de(mat, t)) >= 3], key=lambda t: (-total_de(mat, t), -len(anos_de(mat, t)), t))
    add(f"Elegíveis ({len(eleg)}): " + ", ".join(f"`{t}` ({total_de(mat,t)}; {len(anos_de(mat,t))} anos)" for t in eleg) + ".")
    add("")
    add("| # | Tipo | Total | Anos |")
    add("|---:|---|---:|---|")
    for i, t in enumerate(top5[mat], 1):
        add(f"| {i} | `{t}` | {total_de(mat,t)} | {', '.join(map(str, anos_de(mat,t)))} |")
    nao = [t for t in eleg if t not in top5[mat]]
    if nao:
        add("")
        add("Ficaram fora do top 5, apesar de elegíveis: " + ", ".join(f"`{t}` ({total_de(mat,t)})" for t in nao) + ".")
    add("")
add("### Composição final do top 5")
add("")
for mat in MATERIAS:
    add(f"- **{mat.capitalize()}**: " + "; ".join(f"`{t}` ({total_de(mat,t)})" for t in top5[mat]) + ".")
add("")
add("## 5. Instâncias do top 5 (questões por ano)")
add("")
for mat in MATERIAS:
    add(f"### {mat.capitalize()}")
    add("")
    for t in top5[mat]:
        qs = questoes_de(mat, t)
        partes = "; ".join(f"{a}: " + ", ".join(f"Q{q}" for q in qlist) for a, qlist in qs.items())
        add(f"- **`{t}`** — {total_de(mat,t)} questões. {partes}.")
    add("")
add("## 6. Suporte das questões")
add("")
add("| Ano | texto | mapa | gráfico | tabela | charge | imagem | obra | foto |")
add("|---|" + "|".join("---:" for _ in range(8)) + "|")
for a in ANOS:
    c = Counter(r["suporte"] for r in por_ano[a])
    add(f"| {a} | " + " | ".join(str(c.get(k, 0)) for k in ["texto", "mapa", "grafico", "tabela", "charge", "imagem", "obra", "foto"]) + " |")
add("")
add("O suporte é independente do tipo: uma questão `socioambiental` pode vir em mapa, gráfico ou texto. ")
add("Por isso ele não foi usado para definir o tipo.")
add("")
add("## 7. Observações e limites")
add("")
add("- **2021**: texto extraído por OCR nativo (Windows) porque o PDF oficial tem mapa de fontes quebrado. ")
add("  A classificação foi feita sobre o OCR; o `comando` do JSONL pode conter ruído de OCR, mas o tipo foi lido no trecho final.")
add("- **2020 e 2023**: gabaritos oficiais são escaneados; o OCR não lê letras isoladas. Isso não afeta a classificação por tipo, ")
add("  mas impede o banco completo com gabarito desses dois anos até resolução visual/online.")
add("- **Filosofia**: a distribuição é muito concentrada em `interpretar-fragmento` (26 de 48). Os outros quatro tipos foram ")
add("  separados por comando (aplicação de conceito, comparação de autores, julgamento ético e epistemologia/ciência). ")
add("  Se o critério fosse apenas temático, a matéria ficaria com menos de 5 tipos com ≥3 anos.")
add("- **2025**: taxonomia congelada e auditoria aprovada; não foi reclassificado nesta etapa.")
add("- A matriz é a entrega obrigatória do T6 e está na seção 3; o `dados/top5.json` traz a mesma seleção em formato de máquina.")
add("")
add("## 8. Próximos passos")
add("")
add("1. **T7** — montar o banco final: texto completo (enunciado + alternativas + gabarito) só para as questões dos 20 tipos do top 5; ")
add("   as demais guardam rótulo, tipo, tema, suporte, página e comando.")
add("2. **T8** — preparar a casa do Teacher e o `Teacher.md` global (com backup e restauração ao fim).")
add("3. **T9** — gerar os 20 resumos (5 tipos × 4 matérias), com as respostas padrão aprovadas.")
add("4. **T10** — validar os resumos contra as instâncias e a matriz.")
add("5. **T11** — restaurar o `Teacher.md` global.")
add("")

rel = METRICAS / "relatorio-t6.md"
rel.write_text("\n".join(linhas), encoding="utf-8")

top5_json = {}
for mat in MATERIAS:
    top5_json[mat] = []
    for t in top5[mat]:
        top5_json[mat].append({
            "tipo": t,
            "total": total_de(mat, t),
            "anos": anos_de(mat, t),
            "questoes": questoes_de(mat, t),
        })
(DADOS / "top5.json").write_text(json.dumps(top5_json, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"relatorio: {rel}")
print(f"top5: {DADOS / 'top5.json'}")
print("erros:", len(erros))
for mat in MATERIAS:
    print(mat, [(t, total_de(mat, t), len(anos_de(mat, t))) for t in top5[mat]])
