# split_questoes.py - divide o texto extraido de cada ano em questoes 46-90.
# Gera dados/questoes_<ano>_split.json  { "46": "...", ..., "90": "..." }
import json
import re
from pathlib import Path

base = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
txt = base / "dados" / "texto"
out_dir = base / "dados"

# fontes: 2021 usa OCR; demais usam PyMuPDF
fontes = {
    2020: txt / "2020_Humanas_Prova.txt",
    2021: txt / "2021_ocr.txt",
    2022: txt / "2022_Humanas_Prova.txt",
    2023: txt / "2023_Humanas_Prova.txt",
    2024: txt / "2024_Humanas_Prova.txt",
}

def limpar(t: str) -> str:
    t = t.replace("\ufb01", "fi").replace("\ufb02", "fl")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

for ano, caminho in fontes.items():
    if not caminho.exists():
        print(f"{ano}: FALTA {caminho.name}")
        continue
    texto = limpar(caminho.read_text(encoding="utf-8", errors="replace"))
    # cabeçalhos: Questão 46 / QUESTÃO 46 / Questao 46
    pat = re.compile(r"(?:QUEST[ÃA]O|Quest[ÃAãa]o)\s*0*(\d{1,2})\b")
    marcas = []
    for m in pat.finditer(texto):
        q = int(m.group(1))
        if 46 <= q <= 90:
            marcas.append((q, m.start(), m.end()))
    # remove duplicatas mantendo a primeira ocorrência de cada q
    vistos = {}
    for q, ini, fim in marcas:
        if q not in vistos:
            vistos[q] = (ini, fim)
    dados = {}
    for q in range(46, 91):
        if q not in vistos:
            continue
        ini, fim = vistos[q]
        prox = min([v[0] for k, v in vistos.items() if k > q] or [len(texto)])
        dados[str(q)] = texto[fim:prox].strip()
    destino = out_dir / f"questoes_{ano}_split.json"
    destino.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    faltando = [q for q in range(46, 91) if str(q) not in dados]
    print(f"{ano}: {len(dados)}/45  faltando={faltando}  -> {destino.name}")
