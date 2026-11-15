#!/usr/bin/env python3
"""G1 覆蓋率關卡：內容頁至少 1 張 A 級卡；全份至少 3 篇不同來源；卡片都找得到。不足 → exit 1 停下。"""
import re, sys
from pathlib import Path
T = Path(sys.argv[1]); s = (T/"sources.md").read_text(encoding="utf-8")
SKIP = {"01", "10", "12"}  # 封面、測驗、參考資料
fails, all_src = [], set()
for sec in re.split(r"^## ", s, flags=re.M)[1:]:
    nn = sec[:2]; cards = re.findall(r"^### (\S+?)（(\w) 級）\n(.*?)(?=^### |\Z)", sec, re.S | re.M)
    for cid, g, body in cards:
        all_src.add(cid.rsplit("-", 1)[0])
        if body.strip() == "None": fails.append(f"{nn}: 卡片 {cid} 找不到")
    if nn not in SKIP and not any(g == "A" for _, g, _ in cards):
        fails.append(f"{nn}: 沒有 A 級證據 → 退回 N1 補檢索")
if len(all_src) < 3: fails.append(f"全份只有 {len(all_src)} 篇來源（<3）→ 停下回報")
print(f"G1 覆蓋率：{len(all_src)} 篇來源")
print("\n".join(fails) if fails else "✓ G1 通過"); sys.exit(1 if fails else 0)
