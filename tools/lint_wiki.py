#!/usr/bin/env python3
"""Wiki 健康檢查（AGENTS.md 第 9 節 a–e 項）。
用法：python3 tools/lint_wiki.py      全過時 exit 0，有問題時 exit 1。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
LINK = re.compile(r"\[\[([^\]#|]+)(?:#([^\]|]+))?(?:\|[^\]]*)?\]\]")
CLAIM = re.compile(r"研究(顯示|證明|發現|指出)|統合分析|效果量|\d+(\.\d+)?\s*%")
QUOTE = re.compile(r"原文：「([^」]+)」")

problems = []


def report(kind, path, msg):
    problems.append(f"[{kind}] {path.relative_to(ROOT)}: {msg}")


def front(text):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta


pages = {p.relative_to(WIKI).with_suffix("").as_posix(): p for p in WIKI.rglob("*.md")}
texts = {k: p.read_text(encoding="utf-8") for k, p in pages.items()}

# 證據卡的錨點與等級
anchors, grades = {}, {}
for key, text in texts.items():
    if key.startswith("cards/"):
        anchors[key] = set(re.findall(r"^## (\S+)", text, re.M))
for key, text in texts.items():
    if key.startswith("sources/"):
        grades[key.split("/", 1)[1]] = front(text).get("grade", "?")

# (a) 斷掉的連結
inbound = {k: 0 for k in pages}
for key, text in texts.items():
    for target, anchor in LINK.findall(text):
        target = target.strip()
        if target not in pages:
            report("a 斷連結", pages[key], f"[[{target}]] 指向不存在的頁面")
            continue
        if target != key:
            inbound[target] += 1
        if anchor and target.startswith("cards/") and anchor not in anchors.get(target, set()):
            report("a 斷連結", pages[key], f"[[{target}#{anchor}]] 找不到這條證據")

# (b) 孤兒頁：沒有任何頁面連到它，或沒有登記在 index.md（index、log 除外）
# v2（第 1 篇 ingest 後修正）：原本只看「有沒有被連到」，頁面互相連結就會漏掉沒登記 index 的頁面
indexed = {t.strip() for t, _ in LINK.findall(texts.get("index", ""))}
for key, n in inbound.items():
    if key in ("index", "log"):
        continue
    if n == 0:
        report("b 孤兒頁", pages[key], "沒有任何頁面連到這頁")
    if key not in indexed:
        report("b 孤兒頁", pages[key], "沒有登記在 index.md")

# (c) 無出處的說法 與 (d) 可信度違規
for key, text in texts.items():
    if not key.split("/")[0] in ("concepts", "advice", "debates"):
        continue
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    for i, line in enumerate(body.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        cites = [t for t, _ in LINK.findall(line) if t.startswith("cards/")]
        if CLAIM.search(line) and not cites:
            report("c 無出處", pages[key], f"第 {i} 行有研究說法或數字但沒有證據卡：{line.strip()[:40]}…")
        # v2（批次 ingest 後修正）：C 級只能出現在對照頁；其他頁面引用 C 級一律算違規
        c_cites = [t for t in cites if grades.get(t.split("/", 1)[1]) == "C"]
        if key == "debates/internet-vs-research":
            continue
        if c_cites:
            report("d 可信度", pages[key], f"第 {i} 行在對照頁以外引用 C 級來源：{line.strip()[:40]}…")
        elif re.search(r"\d+(\.\d+)?\s*%|\d+\s*(篇|項|人|筆|個實驗)", line) and cites:
            if all(grades.get(t.split("/", 1)[1]) == "B" for t in cites):
                report("d 可信度", pages[key], f"第 {i} 行的數字只用 B 級來源：{line.strip()[:40]}…")

# (e) 原文引用規則
for key, text in texts.items():
    if not key.startswith("cards/"):
        continue
    sid = key.split("/", 1)[1]
    quotes = QUOTE.findall(text)
    if len(quotes) > 1:
        report("e 引文", pages[key], f"一篇資料最多 1 句原文，目前有 {len(quotes)} 句")
    raw = RAW / f"{sid}.md"
    raw_text = raw.read_text(encoding="utf-8") if raw.exists() else ""
    if not raw_text:
        report("e 引文", pages[key], f"找不到 raw/{sid}.md")
    for q in quotes:
        n = len(q.split())
        if n > 15:
            report("e 引文", pages[key], f"原文 {n} 個字，超過 15 字：{q[:30]}…")
        if q not in raw_text or "quote_verified: yes" not in raw_text:
            report("e 引文", pages[key], f"原文沒有在 raw/{sid}.md 中驗證：{q[:30]}…")
    if sid not in grades:
        report("e 引文", pages[key], f"缺少 sources/{sid}.md（無法判斷等級）")

if problems:
    print(f"✗ lint 發現 {len(problems)} 個問題")
    print("\n".join(problems))
    sys.exit(1)
print(f"✓ lint 全過（{len(pages)} 頁，{sum(len(v) for v in anchors.values())} 條證據）")
