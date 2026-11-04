# extract_pymupdf.py - extrai texto dos PDFs de Humanas (prova + gabarito, 2020-2025) via PyMuPDF.
# Saida: <project>\dados\texto\<ano>_Humanas_<Prova|Gabarito>.txt  (UTF-8, com marcadores de pagina)
# Auto-seleciona a melhor fonte: pasta do ano do usuario vs. originais baixados (dados\originais),
# escolhendo o arquivo com MAIS paginas (protege contra downloads incompletos).
import re
from pathlib import Path
import pymupdf

root = Path(r"C:\Users\Luca\Documents\ENEM")
proj = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
out_dir = proj / "dados" / "texto"
orig_dir = proj / "dados" / "originais"
out_dir.mkdir(parents=True, exist_ok=True)

def better_source(year, kind):
    candidates = [root / str(year) / f"{year}_Humanas_{kind}.pdf"]
    if orig_dir.exists():
        candidates += sorted(orig_dir.glob(f"{year}_Humanas_{kind}.pdf"))
    best_path, best_pages = None, -1
    for c in candidates:
        if c.exists():
            try:
                d = pymupdf.open(c); n = d.page_count; d.close()
            except Exception:
                n = -1
            if n > best_pages:
                best_path, best_pages = c, n
    return best_path, best_pages

years = [2020, 2021, 2022, 2023, 2024, 2025]
kinds = ["Prova", "Gabarito"]
print("=== EXTRACAO (PyMuPDF) ===")
for y in years:
    for k in kinds:
        src, npages = better_source(y, k)
        if src is None:
            print(f"{y} {k}: SEM ARQUIVO")
            continue
        doc = pymupdf.open(src)
        pages = [doc[i].get_text() for i in range(doc.page_count)]
        text = "\n\n".join(f"=== PAGINA {i+1} ===\n{t}" for i, t in enumerate(pages))
        dst = out_dir / f"{y}_Humanas_{k}.txt"
        dst.write_text(text, encoding="utf-8")
        found = [q for q in range(46, 91) if re.search(rf"QUEST[\u00c3A]O\s*0*{q}\b", text, re.I)]
        boundary_footer = None
        for i, t in enumerate(pages, 1):
            if re.search(r"CI[\u00caE]NCIAS HUMANAS[^\n]{0,40}\|", t, re.I):
                boundary_footer = i; break
        first_q46 = None
        for i, t in enumerate(pages, 1):
            if re.search(r"QUEST[\u00c3A]O\s*46\b", t, re.I):
                first_q46 = i; break
        missing = [q for q in range(46, 91) if q not in found]
        tail = "..." if len(missing) > 12 else ""
        print(f"{y} {k}: src={src.name} paginas={doc.page_count} chars={len(text)} "
              f"Q46-90_encontradas={len(found)}/45 boundary_footer_pg={boundary_footer} "
              f"primeira_pg_Q46={first_q46} faltando={missing[:12]}{tail}")
        doc.close()
print("=== FIM ===")
