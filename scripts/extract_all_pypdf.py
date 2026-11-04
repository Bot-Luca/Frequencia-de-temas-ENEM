# extract_all_pypdf.py - extrai texto dos PDFs de Humanas (prova + gabarito, 2020-2025) via pypdf.
# Saida: <project>\dados\texto\<ano>_Humanas_<Prova|Gabarito>.txt  (UTF-8, com marcadores de pagina)
import re
from pathlib import Path
from pypdf import PdfReader

root = Path(r"C:\Users\Luca\Documents\ENEM")
proj = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
out_dir = proj / "dados" / "texto"
out_dir.mkdir(parents=True, exist_ok=True)

years = [2020, 2021, 2022, 2023, 2024, 2025]
kinds = ["Prova", "Gabarito"]

print("=== EXTRACAO TEXTO (pypdf) ===")
for y in years:
    for k in kinds:
        src = root / str(y) / f"{y}_Humanas_{k}.pdf"
        if not src.exists():
            print(f"MISSING {src}")
            continue
        dst = out_dir / f"{y}_Humanas_{k}.txt"
        try:
            reader = PdfReader(str(src))
            chunks = []
            for i, page in enumerate(reader.pages, 1):
                try:
                    t = page.extract_text() or ""
                except Exception as e:
                    t = f"[ERRO pagina {i}: {e}]"
                chunks.append(f"=== PAGINA {i} ===\n{t}")
            text = "\n\n".join(chunks)
            dst.write_text(text, encoding="utf-8")
            nq = len(re.findall(r"Quest[a\u00e3]o\s*\d+", text))
            has46 = "SIM" if re.search(r"Quest[a\u00e3]o\s*46", text) else "NAO"
            has90 = "SIM" if re.search(r"Quest[a\u00e3]o\s*90", text) else "NAO"
            print(f"OK {y} {k}: paginas={len(reader.pages)} chars={len(text)} questoes={nq} Q46={has46} Q90={has90}")
        except Exception as e:
            print(f"ERRO {y} {k}: {type(e).__name__}: {e}")
print("=== FIM ===")
