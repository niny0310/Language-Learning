#!/usr/bin/env python3
"""N1 檢索：依 plan.md，從 wiki 頁面收集每頁引用到的證據卡，寫成 sources.md（證據包）。"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
T = ROOT / sys.argv[1]
LINK = re.compile(r"\[\[cards/([^\]#]+)#([^\]]+)\]\]")
def card(sid, cid):
    t = (ROOT/"wiki/cards"/f"{sid}.md").read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(cid)}\n(.*?)(?=^## |\Z)", t, re.S | re.M)
    return m.group(1).strip() if m else None
def grade(sid):
    m = re.search(r"^grade: (\w)", (ROOT/"wiki/sources"/f"{sid}.md").read_text(encoding="utf-8"), re.M); return m.group(1)
out = ["# 證據包（由 tools/retrieve.py 產生，N3 只能引用這裡的卡片）", ""]
for line in (T/"plan.md").read_text(encoding="utf-8").splitlines():
    if not re.match(r"^\d\d \|", line): continue
    nn, title, pages = [x.strip() for x in line.split("|")]
    out.append(f"## {nn} {title}")
    seen = []
    for pg in [p.strip() for p in pages.split(",") if p.strip() != "-"]:
        for sid, cid in LINK.findall((ROOT/"wiki"/f"{pg}.md").read_text(encoding="utf-8")):
            if cid not in seen: seen.append(cid); out.append(f"### {cid}（{grade(sid)} 級）\n{card(sid, cid)}\n")
    if not seen: out.append("（本頁不需證據）\n")
(T/"sources.md").write_text("\n".join(out), encoding="utf-8")
print("sources.md written")
