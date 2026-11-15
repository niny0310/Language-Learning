# Commit 歷史（由本機 git 匯出）

> 本專案在本機用 git 版本控制，每個 ingest 批次、每次修正都有 commit。
> 因為改用 GitHub 網頁上傳，GitHub 上看不到原始 commit，所以把 `git log` 匯出成這份檔案保存。

| # | commit | 時間 | 內容 | 變更檔案數 |
|---|---|---|---|---|
| 1 | `6f3866d` | 2026-11-15 12:55 | 建立 Wiki 骨架：AGENTS.md、訪談紀錄、lint 腳本 | 6 |
| 2 | `4897c5b` | 2026-11-15 12:56 | ingest #1: Dunlosky 2013；修正 lint 孤兒頁檢查（需登記 index） | 9 |
| 3 | `6d29c82` | 2026-11-15 12:57 | ingest #2: Karpicke & Roediger 2008 | 6 |
| 4 | `e675fef` | 2026-11-15 13:05 | 批次 ingest #3-#12（10 篇）；新增 build_index；AI 審查 3 輪；lint (d) 規則修正 | 51 |
| 5 | `8c82d1f` | 2026-11-15 13:06 | 簡報 graph：workflow、N1 檢索、G1 覆蓋率關卡、N2 大綱 v1 | 6 |
| 6 | `d95030b` | 2026-11-15 13:48 | 簡報 N3 逐頁稿＋G2 忠實度審查 3 輪 | 14 |
| 7 | `0b741a4` | 2026-11-15 13:51 | 簡報 N4 渲染＋G3 渲染檢查；README、流程圖、Pages 入口 | 26 |
| 8 | `dbddfaa` | 2026-11-15 13:52 | 繳交草稿、反思草稿 | 3 |

## 各 commit 改了哪些檔案

### `6f3866d` 建立 Wiki 骨架：AGENTS.md、訪談紀錄、lint 腳本
```
AGENTS.md          |  78 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 CLAUDE.md          |   1 +
 docs/interview.md  |  21 +++++++++++++++++++
 tools/lint_wiki.py | 104 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 wiki/index.md      |  11 ++++++++++
 wiki/log.md        |   3 +++
 6 files changed, 218 insertions(+)
```

### `4897c5b` ingest #1: Dunlosky 2013；修正 lint 孤兒頁檢查（需登記 index）
```
raw/dunlosky2013.md                     | 27 +++++++++++++++++++++++++++
 tools/lint_wiki.py                      | 12 +++++++++---
 wiki/cards/dunlosky2013.md              | 42 ++++++++++++++++++++++++++++++++++++++++++
 wiki/concepts/rereading-highlighting.md | 11 +++++++++++
 wiki/concepts/retrieval-practice.md     | 14 ++++++++++++++
 wiki/concepts/spaced-practice.md        | 13 +++++++++++++
 wiki/index.md                           |  7 +++++++
 wiki/log.md                             |  3 +++
 wiki/sources/dunlosky2013.md            | 13 +++++++++++++
 9 files changed, 139 insertions(+), 3 deletions(-)
```

### `6d29c82` ingest #2: Karpicke & Roediger 2008
```
raw/karpicke2008.md                 | 22 ++++++++++++++++++++++
 wiki/cards/karpicke2008.md          | 32 ++++++++++++++++++++++++++++++++
 wiki/concepts/retrieval-practice.md |  6 ++++++
 wiki/index.md                       |  2 ++
 wiki/log.md                         |  3 +++
 wiki/sources/karpicke2008.md        | 13 +++++++++++++
 6 files changed, 78 insertions(+)
```

### `e675fef` 批次 ingest #3-#12（10 篇）；新增 build_index；AI 審查 3 輪；lint (d) 規則修正
```
AGENTS.md                               |  9 +++++----
 raw/aps2016.md                          | 19 +++++++++++++++++++
 raw/clozemaster2026.md                  | 22 ++++++++++++++++++++++
 raw/kimwebb2022.md                      | 22 ++++++++++++++++++++++
 raw/krashen1982.md                      | 22 ++++++++++++++++++++++
 raw/leireynolds2022.md                  | 23 +++++++++++++++++++++++
 raw/nguyen2025.md                       | 22 ++++++++++++++++++++++
 raw/peker2020.md                        | 21 +++++++++++++++++++++
 raw/settles2016.md                      | 21 +++++++++++++++++++++
 raw/soderstrom2016.md                   | 21 +++++++++++++++++++++
 raw/webb2023.md                         | 22 ++++++++++++++++++++++
 tools/build_index.py                    | 18 ++++++++++++++++++
 tools/lint_wiki.py                      | 12 +++++++++---
 wiki/advice/dramas-and-kpop.md          |  8 ++++++++
 wiki/advice/speaking-practice.md        |  7 +++++++
 wiki/advice/vocab-review-routine.md     | 13 +++++++++++++
 wiki/cards/aps2016.md                   | 12 ++++++++++++
 wiki/cards/clozemaster2026.md           | 27 +++++++++++++++++++++++++++
 wiki/cards/dunlosky2013.md              | 10 +++++-----
 wiki/cards/karpicke2008.md              |  8 ++++----
 wiki/cards/kimwebb2022.md               | 27 +++++++++++++++++++++++++++
 wiki/cards/krashen1982.md               | 27 +++++++++++++++++++++++++++
 wiki/cards/leireynolds2022.md           | 32 ++++++++++++++++++++++++++++++++
 wiki/cards/nguyen2025.md                | 27 +++++++++++++++++++++++++++
 wiki/cards/peker2020.md                 | 27 +++++++++++++++++++++++++++
 wiki/cards/settles2016.md               | 27 +++++++++++++++++++++++++++
 wiki/cards/soderstrom2016.md            | 22 ++++++++++++++++++++++
 wiki/cards/webb2023.md                  | 37 +++++++++++++++++++++++++++++++++++++
 wiki/concepts/comprehensible-input.md   | 19 +++++++++++++++++++
 wiki/concepts/flashcards.md             | 14 ++++++++++++++
 wiki/concepts/incidental-learning.md    | 19 +++++++++++++++++++
 wiki/concepts/output.md                 | 13 +++++++++++++
 wiki/concepts/rereading-highlighting.md | 11 +++++++++--
 wiki/concepts/retrieval-practice.md     | 16 +++++++++++-----
 wiki/concepts/spaced-practice.md        | 19 +++++++++++++++----
 wiki/concepts/srs-algorithms.md         | 16 ++++++++++++++++
 wiki/debates/input-vs-output.md         | 24 ++++++++++++++++++++++++
 wiki/debates/internet-vs-research.md    | 10 ++++++++++
 wiki/debates/why-testing-works.md       | 20 ++++++++++++++++++++
 wiki/index.md                           | 49 +++++++++++++++++++++++++++++++++++++++++--------
 wiki/log.md                             | 12 ++++++++++++
 wiki/sources/aps2016.md                 | 13 +++++++++++++
 wiki/sources/clozemaster2026.md         | 13 +++++++++++++
 wiki/sources/kimwebb2022.md             | 13 +++++++++++++
 wiki/sources/krashen1982.md             | 13 +++++++++++++
 wiki/sources/leireynolds2022.md         | 13 +++++++++++++
 wiki/sources/nguyen2025.md              | 13 +++++++++++++
 wiki/sources/peker2020.md               | 13 +++++++++++++
 wiki/sources/settles2016.md             | 13 +++++++++++++
 wiki/sources/soderstrom2016.md          | 13 +++++++++++++
 wiki/sources/webb2023.md                | 13 +++++++++++++
 51 files changed, 902 insertions(+), 35 deletions(-)
```

### `8c82d1f` 簡報 graph：workflow、N1 檢索、G1 覆蓋率關卡、N2 大綱 v1
```
.agents/workflows/topic-slides.md  |  36 ++++++
 tools/gate_coverage.py             |  17 +++
 tools/retrieve.py                  |  25 ++++
 topic-language-learning/outline.md |  24 ++++
 topic-language-learning/plan.md    |  14 +++
 topic-language-learning/sources.md | 477 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 6 files changed, 593 insertions(+)
```

### `d95030b` 簡報 N3 逐頁稿＋G2 忠實度審查 3 輪
```
docs/interview.md                    |  6 ++++++
 tools/check_drafts.py                | 39 +++++++++++++++++++++++++++++++++++++++
 topic-language-learning/drafts/01.md |  6 ++++++
 topic-language-learning/drafts/02.md |  8 ++++++++
 topic-language-learning/drafts/03.md |  9 +++++++++
 topic-language-learning/drafts/04.md |  9 +++++++++
 topic-language-learning/drafts/05.md |  9 +++++++++
 topic-language-learning/drafts/06.md |  9 +++++++++
 topic-language-learning/drafts/07.md |  9 +++++++++
 topic-language-learning/drafts/08.md | 10 ++++++++++
 topic-language-learning/drafts/09.md | 15 +++++++++++++++
 topic-language-learning/drafts/10.md | 18 ++++++++++++++++++
 topic-language-learning/drafts/11.md | 17 +++++++++++++++++
 topic-language-learning/drafts/12.md |  4 ++++
 14 files changed, 168 insertions(+)
```

### `0b741a4` 簡報 N4 渲染＋G3 渲染檢查；README、流程圖、Pages 入口
```
.nojekyll                                       |   0
 README.md                                       |  36 ++++++++++++++
 docs/graph.dot                                  |  22 +++++++++
 docs/graph.png                                  | Bin 0 -> 207300 bytes
 index.html                                      |   2 +
 tools/build_deck.py                             | 172 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tools/check_deck.py                             |  47 ++++++++++++++++++
 topic-language-learning/deck.html               |  50 +++++++++++++++++++
 topic-language-learning/report.md               |  33 +++++++++++++
 topic-language-learning/screens/01.png          | Bin 0 -> 64597 bytes
 topic-language-learning/screens/02.png          | Bin 0 -> 91442 bytes
 topic-language-learning/screens/03-sources.png  | Bin 0 -> 199047 bytes
 topic-language-learning/screens/03.png          | Bin 0 -> 116014 bytes
 topic-language-learning/screens/04.png          | Bin 0 -> 101180 bytes
 topic-language-learning/screens/05.png          | Bin 0 -> 121232 bytes
 topic-language-learning/screens/06.png          | Bin 0 -> 106802 bytes
 topic-language-learning/screens/07.png          | Bin 0 -> 136450 bytes
 topic-language-learning/screens/08.png          | Bin 0 -> 125951 bytes
 topic-language-learning/screens/09.png          | Bin 0 -> 148451 bytes
 topic-language-learning/screens/10-answered.png | Bin 0 -> 151473 bytes
 topic-language-learning/screens/10.png          | Bin 0 -> 116876 bytes
 topic-language-learning/screens/11.png          | Bin 0 -> 169961 bytes
 topic-language-learning/screens/12.png          | Bin 0 -> 238244 bytes
 topic-language-learning/sources.md              |   6 +++
 wiki/advice/vocab-review-routine.md             |   2 +-
 wiki/log.md                                     |   1 +
 26 files changed, 370 insertions(+), 1 deletion(-)
```

### `dbddfaa` 繳交草稿、反思草稿
```
docs/reflection-draft.md | 22 ++++++++++++++++++++++
 docs/submission.md       | 32 ++++++++++++++++++++++++++++++++
 index.html               |  2 +-
 3 files changed, 55 insertions(+), 1 deletion(-)
```
