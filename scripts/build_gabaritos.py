# build_gabaritos.py - consolida os gabaritos 2020-2025 em dados/gabaritos.json
import json
import re
from pathlib import Path

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
TXT = BASE / "dados" / "texto"

# 2020 e 2023: lidos visualmente das imagens oficiais (gabarito escaneado)
VISUAL = {
    2020: {
        46: "D", 47: "A", 48: "B", 49: "C", 50: "B", 51: "D", 52: "D", 53: "D", 54: "A", 55: "E",
        56: "D", 57: "B", 58: "E", 59: "C", 60: "E", 61: "C", 62: "B", 63: "B", 64: "E", 65: "D",
        66: "E", 67: "B", 68: "D", 69: "E", 70: "E", 71: "C", 72: "B", 73: "C", 74: "C", 75: "C",
        76: "B", 77: "A", 78: "C", 79: "D", 80: "C", 81: "C", 82: "A", 83: "D", 84: "E", 85: "B",
        86: "D", 87: "E", 88: "C", 89: "D", 90: "D",
    },
    2023: {
        46: "C", 47: "D", 48: "A", 49: "E", 50: "E", 51: "C", 52: "A", 53: "B", 54: "A", 55: "A",
        56: "C", 57: "E", 58: "A", 59: "A", 60: "D", 61: "E", 62: "C", 63: "B", 64: "D", 65: "A",
        66: "A", 67: "B", 68: "C", 69: "D", 70: "C", 71: "A", 72: "B", 73: "A", 74: "D", 75: "C",
        76: "D", 77: "E", 78: "A", 79: "B", 80: "A", 81: "A", 82: "B", 83: "C", 84: "D", 85: "D",
        86: "E", 87: "B", 88: "A", 89: "D", 90: "B",
    },
}


def parse_texto(ano: int):
    p = TXT / f"{ano}_Humanas_Gabarito.txt"
    linhas = [l.strip() for l in p.read_text(encoding="utf-8", errors="replace").splitlines()]
    resp = {}
    i = 0
    while i < len(linhas) - 1:
        if re.fullmatch(r"0*(4[6-9]|[5-8]\d|90)", linhas[i]):
            q = int(linhas[i])
            for j in range(i + 1, min(i + 5, len(linhas))):
                if re.fullmatch(r"[A-E]", linhas[j]):
                    resp[q] = linhas[j]
                    break
        i += 1
    return resp


gab = {2020: VISUAL[2020], 2023: VISUAL[2023]}
for ano in [2021, 2022, 2024, 2025]:
    gab[ano] = parse_texto(ano)

problemas = []
for ano in [2020, 2021, 2022, 2023, 2024, 2025]:
    faltando = [q for q in range(46, 91) if q not in gab[ano]]
    invalidos = [q for q, v in gab[ano].items() if v not in "ABCDE"]
    print(ano, len(gab[ano]), "faltando=", faltando, "invalidos=", invalidos)
    if faltando or invalidos:
        problemas.append(ano)

if problemas:
    raise SystemExit(f"Gabaritos incompletos: {problemas}")

saida = BASE / "dados" / "gabaritos.json"
saida.write_text(json.dumps({str(a): {str(q): v for q, v in gab[a].items()} for a in gab}, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK ->", saida)
