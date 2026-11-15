#!/usr/bin/env python3
"""N3 逐頁稿的小 loop 檢查（v2：忠實度檢查往前移）。
每頁檢查：1) 內容句都有出處 2) 出處在本頁證據包內 3) 句中每個數字都出現在引用卡片中 4) C 級只能在第 09 頁。
用法：python3 tools/check_drafts.py topic-language-learning [NN ...]"""
import re, sys
from pathlib import Path
T = Path(sys.argv[1]); only = set(sys.argv[2:])
packs, texts, grades = {}, {}, {}
for sec in re.split(r"^## ", (T/"sources.md").read_text(encoding="utf-8"), flags=re.M)[1:]:
    nn = sec[:2]; packs[nn] = set()
    for cid, g, body in re.findall(r"^### (\S+?)（(\w) 級）\n(.*?)(?=^### |\Z)", sec, re.S | re.M):
        packs[nn].add(cid); texts[cid] = body; grades[cid] = g
packs["10"] = packs["03"] | packs["04"] | packs["08"]   # 測驗頁只能用這三頁的證據
# v2（第 1 輪後）：使用者自己的學習狀況來自訪談紀錄，只能用在第 11 頁
packs["11"].add("interview"); texts["interview"] = (T.parent/"docs/interview.md").read_text(encoding="utf-8"); grades["interview"] = "U"
NEEDS = re.compile(r"^(- |why:|both:|internet:)")
NUM = re.compile(r"\d[\d,\.]*")
fails = []
for f in sorted((T/"drafts").glob("*.md")):
    nn = f.stem
    if only and nn not in only: continue
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        cites = [c.strip() for grp in re.findall(r"\{([^}]+)\}", line) for c in grp.split(",")]
        text = re.sub(r"\{[^}]+\}", "", line)
        if NEEDS.match(line) and not cites:
            fails.append(f"{nn}:{i} 沒有出處：{text[:30]}"); continue
        for c in cites:
            if c not in packs.get(nn, set()):
                fails.append(f"{nn}:{i} 引用 {c} 不在本頁證據包"); continue
            if grades[c] == "C" and nn != "09":
                fails.append(f"{nn}:{i} C 級 {c} 只能出現在第 09 頁")
        if cites and all(c in texts for c in cites):
            pool = " ".join(texts[c] for c in cites)
            years = {re.search(r"(\d{4})", c).group(1) for c in cites if re.search(r"\d{4}", c)}  # 來源發表年
            for n in NUM.findall(text):
                n = n.rstrip(".,")
                if n and n not in pool and n not in years:
                    fails.append(f"{nn}:{i} 數字「{n}」不在引用卡片中：{text[:30]}")
print("\n".join(fails) if fails else "✓ 逐頁稿檢查通過"); sys.exit(1 if fails else 0)
