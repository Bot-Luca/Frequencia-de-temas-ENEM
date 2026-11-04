# build_banco.py - banco final: texto completo so para os tipos do top5; rotulo para os demais.
import json
import re
from pathlib import Path

BASE = Path(r"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA")
DADOS = BASE / "dados"
ANOS = [2020, 2021, 2022, 2023, 2024, 2025]

top5 = json.loads((DADOS / "top5.json").read_text(encoding="utf-8"))
top5_set = {(mat, item["tipo"]) for mat, itens in top5.items() for item in itens}
gab = json.loads((DADOS / "gabaritos.json").read_text(encoding="utf-8"))

PUA = {
    "\ue025": "fi", "\ue026": "fi", "\ue01f": "fi", "\ue06d": "fi", "\ue066": "fi",
    "\ue065": "fi", "\ue05b": "fi", "\ue067": "fl", "\ue06e": "fl", "\ue027": "fl", "\ue05c": "fl",
}


def limpar(t: str) -> str:
    for k, v in PUA.items():
        t = t.replace(k, v)
    # remove Private Use Area remanescente (rotulos de grafico sem mapa)
    t = "".join(ch if not (0xE000 <= ord(ch) <= 0xF8FF) else "" for ch in t)
    t = t.replace("\r", "\n")
    t = re.sub(r"===+ PAGINA \d+.*?===+", "", t)
    t = re.sub(r"===== PAGINA \d+.*?=====", "", t)
    t = re.sub(r"PAGINA \d+ \(COLUNA [A-Z]+\)", "", t)
    t = re.sub(r"(?m)^\s*(?:CH|LC) - 1° dia.*$", "", t)
    t = re.sub(r"(?m)^\s*\*?\d{6}[A-Z]{2}\d{2}\*?\s*$", "", t)
    t = re.sub(r"(?m)^\s*Exame Nacional do E(?:\s+enem\d{4})?/?\s*", "", t)
    t = re.sub(r"(?m)^\s*enem20\d\d/?\s*", "", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def parse_alternativas(texto: str):
    linhas = [l.strip() for l in texto.splitlines()]

    # funde "A" sozinho com a linha seguinte "A texto" (layout de 2022/2023)
    merged = []
    i = 0
    while i < len(linhas):
        m = re.match(r"^([A-E])\s*$", linhas[i])
        if m and i + 1 < len(linhas):
            m2 = re.match(r"^([A-E])\s+(.+)$", linhas[i + 1])
            if m2 and m2.group(1) == m.group(1):
                merged.append(linhas[i + 1])
                i += 2
                continue
        merged.append(linhas[i])
        i += 1

    # acha o ultimo bloco completo A,B,C,D,E em sequencia
    def blocos_a():
        return [i for i, l in enumerate(merged) if re.match(r"^A\s+\S", l)]

    escolhido = None
    for a_idx in reversed(blocos_a()):
        seq = [a_idx]
        letra = "B"
        for j in range(a_idx + 1, len(merged)):
            if re.match(rf"^{letra}\s+\S", merged[j]):
                seq.append(j)
                letra = chr(ord(letra) + 1)
                if letra == "F":
                    break
        if len(seq) == 5:
            escolhido = seq
            break
    if escolhido:
        alt = {}
        for idx, letra in zip(escolhido, "ABCDE"):
            alt[letra] = re.sub(rf"^{letra}\s+", "", merged[idx]).strip()
        if all(alt.values()):
            enunciado = "\n".join(merged[:escolhido[0]]).strip()
            return alt, enunciado

    # fallback para OCR de 2021: alternativas separadas por O/@
    partes = re.split(r"\s+[O@]\s+", texto)
    partes = [p.strip() for p in partes if p.strip()]
    if len(partes) >= 5:
        ult = partes[-5:]
        if all(len(p) <= 260 and p.endswith((".", "?", "!", ":")) for p in ult):
            alt = {letra: re.sub(r"^[O@]\s*", "", p).strip() for letra, p in zip("ABCDE", ult)}
            inicio = texto.rfind(ult[0])
            enunciado = texto[:inicio].strip() if inicio > 0 else texto
            return alt, enunciado
    return None, texto


linhas_saida = []
resumo = {"total": 0, "top5": 0, "rotulo": 0, "por_materia": {}, "por_ano": {}}
for ano in ANOS:
    split = json.loads((DADOS / f"questoes_{ano}_split.json").read_text(encoding="utf-8"))
    for line in (DADOS / f"classificacao_{ano}.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        chave = (r["materia"], r["tipo"])
        eh_top5 = chave in top5_set
        texto = limpar(split.get(str(r["q"]), ""))
        row = {
            "ano": ano,
            "q": r["q"],
            "materia": r["materia"],
            "tipo": r["tipo"],
            "tema": r["tema"],
            "suporte": r["suporte"],
            "tem_imagem": r["tem_imagem"],
            "pagina": r["pagina"],
            "comando": r["comando"],
            "top5": eh_top5,
        }
        if eh_top5:
            alt, enunciado = parse_alternativas(texto)
            row["gabarito"] = gab[str(ano)][str(r["q"])]
            row["gabarito_fonte"] = (
                "INEP — gabarito oficial escaneado (leitura visual)"
                if ano in (2020, 2023)
                else "INEP — gabarito oficial em texto"
            )
            row["fonte"] = f"INEP — ENEM {ano}, Dia 1, Caderno 1 (Azul), Q{r['q']}, p. {r['pagina']}"
            row["qualidade_texto"] = "ocr" if ano == 2021 else ("transcricao" if ano == 2025 else "pdf")
            row["enunciado"] = enunciado
            row["alternativas"] = alt
            row["texto_completo"] = texto
            if alt is None:
                row["obs_texto"] = "Alternativas não separadas automaticamente; ver texto_completo."
            resumo["top5"] += 1
        else:
            resumo["rotulo"] += 1
        resumo["total"] += 1
        resumo["por_materia"][r["materia"]] = resumo["por_materia"].get(r["materia"], 0) + 1
        resumo["por_ano"][str(ano)] = resumo["por_ano"].get(str(ano), 0) + 1
        linhas_saida.append(row)

saida = DADOS / "banco_questoes.jsonl"
with saida.open("w", encoding="utf-8", newline="\n") as f:
    for row in linhas_saida:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

(DADOS / "banco_resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
print("banco:", saida)
print("resumo:", resumo)
print("top5 por materia:", {m: sum(1 for x in linhas_saida if x["materia"] == m and x["top5"]) for m in ["historia", "geografia", "filosofia", "sociologia"]})
