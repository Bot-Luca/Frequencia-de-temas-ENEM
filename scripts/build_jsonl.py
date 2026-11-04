# build_jsonl.py - monta dados/classificacao_<ano>.jsonl a partir de um arquivo de rotulos.
# Formato do rotulo: q|materia|tipo|suporte|tema1;tema2;tema3
# uso: python build_jsonl.py ANO
import json
import re
import sys
from pathlib import Path

ANO = int(sys.argv[1])
BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
DADOS = BASE / "dados"
ROTULOS = BASE / "classificacoes" / f"{ANO}.txt"

FONTES = {
    2020: DADOS / "texto" / "2020_Humanas_Prova.txt",
    2021: DADOS / "texto" / "2021_ocr.txt",
    2022: DADOS / "texto" / "2022_Humanas_Prova.txt",
    2023: DADOS / "texto" / "2023_Humanas_Prova.txt",
    2024: DADOS / "texto" / "2024_Humanas_Prova.txt",
}

split = json.loads((DADOS / f"questoes_{ANO}_split.json").read_text(encoding="utf-8"))
fonte = FONTES[ANO].read_text(encoding="utf-8", errors="replace")


def paginas_por_questao(texto: str):
    marcas_pg = [(m.start(), int(m.group(1))) for m in re.finditer(r"PAGINA\s+(\d+)", texto)]
    mapa = {}
    for q in range(46, 91):
        pat = re.compile(rf"(?:QUEST[ÃA]O|Quest[ÃAãa]o)\s*0*{q}\b")
        m = pat.search(texto)
        if not m:
            continue
        pg = None
        for pos, n in marcas_pg:
            if pos < m.start():
                pg = n
            else:
                break
        mapa[q] = pg
    return mapa


def limpar(t: str) -> str:
    t = t.replace("\ufb01", "fi").replace("\ufb02", "fl")
    t = re.sub(r"===+ PAGINA \d+.*?===+", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def comando_de(t: str) -> str:
    linhas = t.splitlines()
    corte = len(linhas)
    achou = []
    for i, ln in enumerate(linhas):
        m = re.match(r"^\s*([A-E])\s+\S", ln)
        if m:
            achou.append((i, m.group(1)))
    for k in range(len(achou) - 3):
        letras = [b[1] for b in achou[k:k + 5]]
        if letras[:4] == ["A", "B", "C", "D"]:
            corte = achou[k][0]
            break
    stem = limpar(" ".join(linhas[:corte]))
    if not stem:
        stem = limpar(t)
    return stem[-320:]


def detectar_suporte(t: str) -> str:
    s = t.lower()
    regras = [
        ("mapa", ["mapa", "cartograma", "mapas"]),
        ("grafico", ["gráfico", "grafico", "gráficos"]),
        ("tabela", ["tabela", "tabelas"]),
        ("charge", ["charge", "cartum", "tirinha"]),
        ("obra", ["pintura", "quadro", "obra de arte", "escultura"]),
        ("fotografia", ["fotografia", "foto de", "fotógrafo"]),
        ("imagem", ["imagem", "figura", "satélite", "satelite", "propaganda", "cartaz"]),
    ]
    for nome, chaves in regras:
        if any(k in s for k in chaves):
            return nome
    return "texto"


paginas = paginas_por_questao(fonte)
rotulos = {}
for linha in ROTULOS.read_text(encoding="utf-8").splitlines():
    linha = linha.strip()
    if not linha or linha.startswith("#"):
        continue
    q, materia, tipo, suporte, tema = [x.strip() for x in linha.split("|")]
    rotulos[int(q)] = {
        "materia": materia,
        "tipo": tipo,
        "suporte": suporte,
        "tema": [x.strip() for x in tema.split(";") if x.strip()],
    }

saida = DADOS / f"classificacao_{ANO}.jsonl"
faltando = [q for q in range(46, 91) if q not in rotulos]
with saida.open("w", encoding="utf-8", newline="\n") as f:
    for q in range(46, 91):
        r = rotulos.get(q)
        if not r:
            continue
        texto = split.get(str(q), "")
        sup = r["suporte"]
        if sup == "auto":
            sup = detectar_suporte(texto)
        row = {
            "ano": ANO,
            "q": q,
            "materia": r["materia"],
            "tipo": r["tipo"],
            "tema": r["tema"],
            "suporte": sup,
            "tem_imagem": sup not in ("texto", "tabela", "grafico"),
            "pagina": paginas.get(q),
            "comando": comando_de(texto),
            "obs": None,
        }
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print(f"{ANO}: {len(rotulos)}/45 rotulos -> {saida.name}; faltando={faltando}")
