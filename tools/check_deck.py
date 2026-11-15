#!/usr/bin/env python3
"""G3 渲染檢查：「做完了」由這支腳本決定。
檢查：頁數 8–15、內容頁都有出處按鈕、無溢出、稿子每句原文都在 HTML 裡（渲染不准改字）、
測驗可點、鍵盤可翻頁。截圖存到 screens/。用法：python3 tools/check_deck.py topic-language-learning"""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
T = Path(sys.argv[1]).resolve(); (T/"screens").mkdir(exist_ok=True)
fails, log = [], []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 770})
    pg.goto((T/"deck.html").as_uri()); pg.wait_for_timeout(300)
    n = pg.locator(".slide").count(); log.append(f"頁數：{n}")
    if not 8 <= n <= 15: fails.append(f"頁數 {n} 不在 8–15")
    text_all = pg.evaluate("document.getElementById('stage').textContent")
    for k in range(1, n + 1):
        pg.evaluate(f"go({k-1})"); pg.wait_for_timeout(80)
        s = pg.locator(".slide.on")
        nn = s.get_attribute("data-n")
        over = pg.evaluate("""()=>{const r=document.querySelector('.slide.on .inner');
            let o=r.scrollHeight>r.clientHeight+1||r.scrollWidth>r.clientWidth+1;
            r.querySelectorAll('*').forEach(e=>{const a=e.getBoundingClientRect(),c=r.getBoundingClientRect();
              if(a.bottom>c.bottom+1||a.right>c.right+1)o=true});return o}""")
        if over: fails.append(f"{nn}: 內容溢出 → 退回 N3 縮短（N4 不准刪字）")
        if nn not in ("01", "12") and s.locator(".srcbtn").count() == 0: fails.append(f"{nn}: 沒有出處標籤")
        s.screenshot(path=str(T/"screens"/f"{nn}.png"))
    # 稿子每句原文都在 HTML
    for f in sorted((T/"drafts").glob("*.md")):
        for line in f.read_text(encoding="utf-8").split("---", 2)[2].splitlines():
            t = re.sub(r"^(- |> |\w+\*?: )", "", line); t = re.sub(r"\s*\{[^}]+\}", "", t).replace("**", "").strip()
            if t and f.stem != "12" and t not in text_all: fails.append(f"{f.stem}: 渲染後文字被改動：{t[:25]}…")
    # 測驗可點
    pg.evaluate("go(9)"); qs = pg.locator(".slide.on .q")
    for q in range(qs.count()):
        qs.nth(q).locator(".opt").first.click()
        if not qs.nth(q).locator(".why").is_visible(): fails.append(f"10: 第 {q+1} 題點了沒有顯示解答")
    pg.locator(".slide.on").screenshot(path=str(T/"screens"/"10-answered.png"))
    # 出處彈窗
    pg.evaluate("go(2)"); pg.locator(".slide.on .srcbtn").click()
    if not pg.locator(".slide.on .pop").is_visible(): fails.append("03: 出處按鈕點了沒反應")
    pg.locator(".slide.on").screenshot(path=str(T/"screens"/"03-sources.png"))
    # 鍵盤
    pg.evaluate("go(0)"); pg.keyboard.press("ArrowRight")
    if pg.locator(".slide.on").get_attribute("data-n") != "02": fails.append("鍵盤 → 無法翻頁")
    b.close()
log.append("✓ G3 通過" if not fails else f"✗ G3 發現 {len(fails)} 個問題")
print("\n".join(log + fails)); sys.exit(1 if fails else 0)
