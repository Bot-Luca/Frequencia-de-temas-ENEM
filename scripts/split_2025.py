# split_2025.py - converte a transcricao estruturada de 2025 em questoes_2025_split.json
import json
import re
from pathlib import Path

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
p = BASE / "dados" / "questoes_2025_humanas.txt"
t = p.read_text(encoding="utf-8")

blocos = re.split(r"^=== QUESTÃO (\d{2}) ===\s*$", t, flags=re.M)
dados = {}
for i in range(1, len(blocos), 2):
    q = int(blocos[i])
    corpo = blocos[i + 1]
    m = re.search(r"^ENUNCIADO:\s*$", corpo, flags=re.M)
    if not m:
        continue
    fim = re.search(r"^(TIPO_VISUAL|LEGENDA_IMAGEM|OBS):", corpo[m.end():], flags=re.M)
    texto = corpo[m.end(): m.end() + fim.start()] if fim else corpo[m.end():]
    texto = texto.strip()
    # alternativas estruturadas -> formato A ...
    texto = re.sub(r"^ALT_([A-E]):\s*", lambda m: m.group(1) + " ", texto, flags=re.M)
    # legenda de imagem, se houver
    leg = re.search(r"^LEGENDA_IMAGEM:\s*(.+)$", corpo, flags=re.M)
    if leg and leg.group(1).strip():
        texto += "\n\n" + leg.group(1).strip()
    dados[str(q)] = texto.strip()

saida = BASE / "dados" / "questoes_2025_split.json"
saida.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
print("2025:", len(dados), "questoes ->", saida.name)
print("faltando:", [q for q in range(46, 91) if str(q) not in dados])
