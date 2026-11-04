# digest_top5.py - digesto compacto das questoes do top5, por materia e tipo.
import json
from pathlib import Path

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
DADOS = BASE / "dados"
rows = [json.loads(l) for l in (DADOS / "banco_questoes.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
top5 = json.loads((DADOS / "top5.json").read_text(encoding="utf-8"))
MATERIAS = ["historia", "geografia", "filosofia", "sociologia"]


def limpar(t: str) -> str:
    return " ".join((t or "").split())


L = []
add = L.append
for mat in MATERIAS:
    add(f"# {mat.upper()}")
    add("")
    for item in top5[mat]:
        tipo = item["tipo"]
        sub = [r for r in rows if r["materia"] == mat and r["tipo"] == tipo]
        sub.sort(key=lambda r: (r["ano"], r["q"]))
        add(f"## {tipo} — {len(sub)} questões | anos={item['anos']}")
        add("")
        for r in sub:
            cmd = limpar(r.get("comando", ""))[-300:]
            enun = limpar(r.get("enunciado", ""))[:180]
            gab = r.get("gabarito", "-")
            tema = "; ".join(r.get("tema", []))
            add(f"- **{r['ano']} Q{r['q']}** [{r['suporte']}] gab={gab} | tema: {tema}")
            add(f"  - cmd: {cmd}")
            if enun:
                add(f"  - ini: {enun}")
        add("")

out = DADOS / "digest_top5.md"
out.write_text("\n".join(L), encoding="utf-8")
print(out)
print("chars", len("\n".join(L)))
print("linhas", len(L))
