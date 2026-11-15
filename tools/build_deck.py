#!/usr/bin/env python3
"""N4 渲染：把已通過檢查的 drafts/*.md 排版成單一 HTML。只排版，不改任何字。
用法：python3 tools/build_deck.py topic-language-learning"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / sys.argv[1]
CARDS, SRC = {}, {}
for p in (ROOT / "wiki/sources").glob("*.md"):
    t = p.read_text(encoding="utf-8")
    SRC[p.stem] = {
        "title": re.search(r"^# (.+)$", t, re.M).group(1),
        "bib": re.search(r"^- 書目：(.+)$", t, re.M).group(1),
        "grade": re.search(r"^grade: (\w)", t, re.M).group(1),
        "cov": re.search(r"^coverage: (.+)$", t, re.M).group(1),
    }
for p in (ROOT / "wiki/cards").glob("*.md"):
    for cid, body in re.findall(r"^## (\S+)\n(.*?)(?=^## |\Z)", p.read_text(encoding="utf-8"), re.S | re.M):
        g = lambda k: (re.search(rf"^- {k}：(.+)$", body, re.M) or [None, ""])[1]
        CARDS[cid] = {"src": p.stem, "claim": g("說法"), "loc": g("位置"),
                      "quote": g("原文").strip("「」"), "grade": SRC[p.stem]["grade"]}
CARDS["interview"] = {"src": "interview", "claim": "使用者自己的學習狀況（需求訪談）", "loc": "docs/interview.md",
                      "quote": "", "grade": "—"}

def md(s):  # **粗體** 以外不做任何文字轉換
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(s)))

def split_cites(line):
    cites = [c.strip() for grp in re.findall(r"\{([^}]+)\}", line) for c in grp.split(",")]
    return re.sub(r"\s*\{[^}]+\}", "", line).strip(), cites

def parse(path):
    t = path.read_text(encoding="utf-8")
    meta = dict(re.findall(r"^(\w+): (.+)$", t.split("---")[1], re.M))
    body = t.split("---", 2)[2].strip().splitlines()
    return meta, body

def render(nn, meta, body):
    used = []
    def mark(cites):
        nums = []
        for c in cites:
            if c not in used: used.append(c)
            nums.append(used.index(c) + 1)
        return f'<sup class="m">[{",".join(map(str, sorted(nums)))}]</sup>' if nums else ""
    lay, h = meta["layout"], []
    if lay == "title":
        kv = dict(l.split(": ", 1) for l in body if ": " in l)
        h.append(f'<div class="cover"><p class="kicker">生成式 AI 課程｜LLM Wiki 教學簡報</p><h1>{md(meta["title"])}</h1>'
                 f'<p class="sub">{md(kv["subtitle"])}</p><p class="note">{md(kv["note"])}</p>'
                 f'<p class="hint">按 → 或空白鍵開始　·　右下角「出處」可查原文</p></div>')
    elif lay == "bullets":
        h.append(f"<h2>{md(meta['title'])}</h2><ul class='pts'>")
        for l in body:
            if l.startswith("- "):
                txt, c = split_cites(l[2:]); h.append(f"<li>{md(txt)}{mark(c)}</li>")
        h.append("</ul>")
        for l in body:
            if l.startswith("> "):
                txt, c = split_cites(l[2:]); h.append(f'<p class="take">{md(txt)}{mark(c)}</p>')
    elif lay in ("compare", "menu"):
        kv, cols, cur = {}, {"left": [], "right": []}, None
        for l in body:
            m = re.match(r"^(\w+): (.+)$", l)
            if m:
                kv[m.group(1)] = m.group(2)
                if m.group(1).endswith("_title"): cur = m.group(1)[:-6]
            elif l.startswith("- ") and cur:
                cols[cur].append(l[2:])
        h.append(f"<h2>{md(meta['title'])}</h2>")
        if "intro" in kv: h.append(f'<p class="intro">{md(kv["intro"])}</p>')
        h.append(f'<div class="cols {lay}">')
        for side in ("left", "right"):
            h.append(f'<div class="col {side}"><h3>{md(kv[side + "_title"])}</h3><ul>')
            for l in cols[side]:
                txt, c = split_cites(l); h.append(f"<li>{md(txt)}{mark(c)}</li>")
            h.append("</ul></div>")
        h.append("</div>")
        if "both" in kv:
            txt, c = split_cites(kv["both"]); h.append(f'<p class="both">{md(txt)}{mark(c)}</p>')
        if "internet" in kv:
            txt, c = split_cites(kv["internet"]); h.append(f'<p class="net"><span>C 級</span>{md(txt)}{mark(c)}</p>')
        for l in body:
            if l.startswith("> "):
                txt, c = split_cites(l[2:]); h.append(f'<p class="take">{md(txt)}{mark(c)}</p>')
    elif lay == "quiz":
        h.append(f"<h2>{md(meta['title'])}</h2><p class='intro'>先自己想答案再點，這本身就是在練「主動回想」。</p><div class='quiz'>")
        qs, q = [], None
        for l in body:
            if l.startswith("q: "): q = {"q": l[3:], "o": [], "why": ""}; qs.append(q)
            elif l.startswith("o*: "): q["o"].append((l[4:], True))
            elif l.startswith("o: "): q["o"].append((l[3:], False))
            elif l.startswith("why: "): q["why"] = l[5:]
        for i, q in enumerate(qs, 1):
            txt, c = split_cites(q["why"])
            opts = "".join(f'<button class="opt" data-ok="{int(ok)}">{md(o)}</button>' for o, ok in q["o"])
            h.append(f'<div class="q"><p class="qq">Q{i}. {md(q["q"])}</p><div class="opts">{opts}</div>'
                     f'<p class="why" hidden>{md(txt)}{mark(c)}</p></div>')
        h.append("</div>")
    elif lay == "refs":
        h.append(f"<h2>{md(meta['title'])}</h2><ol class='refs'>")
        for sid in sorted(SRC, key=lambda s: (SRC[s]["grade"], s)):
            s = SRC[sid]
            h.append(f'<li><span class="g g{s["grade"]}">{s["grade"]}</span>{md(s["bib"])}<em>讀取範圍：{md(s["cov"])}</em></li>')
        h.append("</ol><p class='legend'>A：同儕審查論文、統合分析、學術著作｜B：大學／學會新聞稿｜C：部落格、App 行銷文（只出現在對照框）</p>")
    pop = ""
    if used:
        items = []
        for i, c in enumerate(used, 1):
            k = CARDS[c]; s = SRC.get(k["src"], {"title": "需求訪談紀錄"})
            q = f'<q>{html.escape(k["quote"])}</q>' if k["quote"] else ""
            items.append(f'<li><b>[{i}] {html.escape(s["title"])}</b> <span class="g g{k["grade"]}">{k["grade"]}</span><br>'
                         f'{html.escape(k["claim"])}{q}<small>{html.escape(c)}｜{html.escape(k["loc"])}</small></li>')
        pop = f'<button class="srcbtn" aria-expanded="false">出處 {len(used)}</button><div class="pop" hidden><ol>{"".join(items)}</ol></div>'
    return f'<section class="slide l-{lay}" data-n="{nn}"><div class="inner">{"".join(h)}</div>{pop}<span class="pg">{int(nn)} / 12</span></section>'

slides = [render(p.stem, *parse(p)) for p in sorted((T / "drafts").glob("*.md"))]
CSS = """
:root{--paper:#f6f1e7;--ink:#1f2a37;--muted:#5b6573;--accent:#c2410c;--teal:#0f766e;--line:#e2d9c8;--card:#fffdf8}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#1b1f24;font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;color:var(--ink)}
#stage{position:fixed;inset:0 0 52px 0;display:grid;place-items:center}
.slide{position:absolute;width:1280px;height:720px;background:var(--paper);display:none;transform-origin:center;border-radius:6px;overflow:hidden}
.slide.on{display:block}.inner{position:absolute;inset:56px 72px 64px;overflow:hidden}
h2+.refs{margin-top:-8px}h1{font-size:68px;line-height:1.15;margin:0 0 24px;letter-spacing:.02em}h2{font-size:40px;margin:0 0 28px;padding-bottom:14px;border-bottom:3px solid var(--accent);display:inline-block}
h3{font-size:22px;margin:0 0 12px;color:var(--teal)}
.cover{height:100%;display:flex;flex-direction:column;justify-content:center}.kicker{color:var(--accent);font-weight:700;letter-spacing:.1em;margin:0 0 18px}
.sub{font-size:30px;margin:0 0 10px}.note{font-size:22px;color:var(--muted);margin:0}.hint{margin-top:56px;color:var(--muted);font-size:16px}
ul{margin:0;padding-left:1.1em}.pts li{font-size:25px;line-height:1.5;margin:0 0 16px}
.take{position:absolute;left:0;right:0;bottom:0;margin:0;background:var(--ink);color:#fff;font-size:22px;padding:14px 22px;border-left:8px solid var(--accent);border-radius:4px}
sup.m{color:var(--accent);font-size:.6em;font-weight:700;margin-left:2px}
.intro{font-size:20px;color:var(--muted);margin:-12px 0 16px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:24px}.col{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:18px 22px}
.col li{font-size:20px;line-height:1.5;margin-bottom:10px}.l-compare .col li{font-size:22px;margin-bottom:14px}
.both{font-size:19px;margin:18px 0 0;color:var(--ink)}.net{font-size:17px;margin:8px 0 0;color:var(--muted)}
.net span{background:#9ca3af;color:#fff;border-radius:3px;padding:1px 6px;margin-right:8px;font-size:13px}
.l-compare .take,.l-menu .take{position:static;margin-top:18px;font-size:20px;padding:10px 18px}
.quiz{display:grid;gap:26px}.qq{font-size:25px;margin:0 0 8px;font-weight:700}.opts{display:flex;gap:10px;flex-wrap:wrap}
.opt{font:inherit;font-size:20px;padding:10px 20px;border:2px solid var(--line);background:var(--card);border-radius:20px;cursor:pointer}
.opt.right{border-color:var(--teal);background:#ccfbf1}.opt.wrong{border-color:#b91c1c;background:#fee2e2}.why{font-size:18px;color:var(--teal);margin:6px 0 0}
.refs{font-size:13.5px;line-height:1.4;margin:0;padding-left:1.4em;columns:2;column-gap:36px}.refs li{margin-bottom:6px;break-inside:avoid}.refs em{display:block;color:var(--muted);font-style:normal;font-size:12.5px}
.legend{font-size:13px;color:var(--muted);margin-top:6px}
.g{display:inline-block;min-width:20px;text-align:center;border-radius:3px;color:#fff;font-size:12px;font-weight:700;margin-right:6px;padding:0 4px}.gA{background:var(--teal)}.gB{background:#b45309}.gC{background:#9ca3af}.g—{background:#64748b}
.srcbtn{position:absolute;right:24px;bottom:18px;font:inherit;font-size:14px;background:var(--card);border:1px solid var(--accent);color:var(--accent);border-radius:14px;padding:4px 14px;cursor:pointer;z-index:3}
.pop{position:absolute;right:24px;bottom:56px;width:560px;max-height:520px;overflow:auto;background:#fff;border:1px solid var(--line);box-shadow:0 10px 30px rgba(0,0,0,.18);border-radius:8px;padding:12px 16px;z-index:4;font-size:14px;line-height:1.5}
.pop ol{margin:0;padding:0;list-style:none}.pop li{padding:8px 0;border-bottom:1px dashed var(--line)}.pop q{display:block;margin:4px 0;font-style:italic;color:var(--teal)}
.pop small{display:block;color:var(--muted)}.pg{position:absolute;left:28px;bottom:20px;color:var(--muted);font-size:14px}
#bar{position:fixed;left:0;top:0;height:4px;background:var(--accent);transition:width .2s;z-index:9}
.nav{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:9}.nav button{font:inherit;background:#334155;color:#fff;border:0;border-radius:16px;padding:6px 16px;cursor:pointer;opacity:.75}
@media print{.nav,#bar,.srcbtn{display:none}}
"""
JS = """
const S=[...document.querySelectorAll('.slide')];let i=0;
function fit(){const k=Math.min(innerWidth/1280,(innerHeight-50)/720);S.forEach(s=>s.style.transform=`scale(${k})`)}
function go(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,j)=>s.classList.toggle('on',j===i));
 document.getElementById('bar').style.width=((i+1)/S.length*100)+'%';try{history.replaceState(null,'','#'+(i+1))}catch(e){}}
addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();go(i+1)}
 if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(i-1)}if(e.key==='Escape')document.querySelectorAll('.pop').forEach(p=>p.hidden=true)});
document.getElementById('prev').onclick=()=>go(i-1);document.getElementById('next').onclick=()=>go(i+1);
document.querySelectorAll('.srcbtn').forEach(b=>b.onclick=e=>{e.stopPropagation();const p=b.nextElementSibling;p.hidden=!p.hidden;b.setAttribute('aria-expanded',!p.hidden)});
document.querySelectorAll('.q').forEach(q=>q.querySelectorAll('.opt').forEach(o=>o.onclick=()=>{
 q.querySelectorAll('.opt').forEach(x=>{x.disabled=true;if(x.dataset.ok==='1')x.classList.add('right')});
 if(o.dataset.ok!=='1')o.classList.add('wrong');q.querySelector('.why').hidden=false}));
addEventListener('resize',fit);fit();go((parseInt(location.hash.slice(1))||1)-1);
"""
out = f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>語言怎麼學才有效？｜LLM Wiki 教學簡報</title><style>{CSS}</style></head><body>
<div id="bar"></div><div id="stage">{''.join(slides)}</div>
<div class="nav"><button id="prev">← 上一頁</button><button id="next">下一頁 →</button></div>
<script>{JS}</script></body></html>"""
(T / "deck.html").write_text(out, encoding="utf-8")
print(f"deck.html：{len(slides)} 頁")
