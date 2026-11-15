#!/usr/bin/env python3
"""由各頁 H1 自動重建 wiki/index.md（ingest 批次後新增：手動登記 index 太容易漏）。"""
import re
from pathlib import Path
W = Path(__file__).resolve().parent.parent / "wiki"
def h1(p):
    m = re.search(r"^# (.+)$", p.read_text(encoding="utf-8"), re.M); return m.group(1) if m else p.stem
def meta(p, k):
    m = re.search(rf"^{k}: (.+)$", p.read_text(encoding="utf-8"), re.M); return m.group(1) if m else "?"
out = ["# Wiki 目錄", "", "> 由 tools/build_index.py 自動產生", ""]
out += ["## 資料來源（sources）", "| 頁面 | 標題 | 等級 | 讀取範圍 |", "|---|---|---|---|"]
for p in sorted((W/"sources").glob("*.md")):
    out.append(f"| [[sources/{p.stem}]] | {h1(p)} | {meta(p,'grade')} | {meta(p,'coverage')} |")
for d, name in [("cards","證據卡"),("concepts","概念"),("advice","學習建議"),("debates","爭議")]:
    out += ["", f"## {name}（{d}）"]
    out += [f"- [[{d}/{p.stem}]] {h1(p)}" for p in sorted((W/d).glob("*.md"))]
(W/"index.md").write_text("\n".join(out)+"\n", encoding="utf-8")
print("index rebuilt")
