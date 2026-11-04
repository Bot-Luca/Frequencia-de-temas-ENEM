import json
from pathlib import Path

p = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA\dados\classificacao_2025.jsonl")
for line in p.read_text(encoding="utf-8").splitlines():
    r = json.loads(line)
    print(f"{r['q']:>2} {r['materia'][:4]:<4} {r['tipo']:<24} | {r['comando'][:110]}")
