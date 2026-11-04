import json
import sys
from pathlib import Path

ano = int(sys.argv[1])
qs = [int(x) for x in sys.argv[2:]]
p = Path(rf"C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA\dados\questoes_{ano}_split.json")
d = json.loads(p.read_text(encoding="utf-8"))
for q in qs:
    t = d.get(str(q), "")
    print(f"===== Q{q} ({len(t)} chars) =====")
    print(t[-900:])
