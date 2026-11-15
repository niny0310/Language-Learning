---
id: settles2016
title: "A Trainable Spaced Repetition Model for Language Learning"
authors: Settles, Meeder
year: 2016
venue: Proceedings of ACL 2016, 1848–1858
doi: 10.18653/v1/P16-1174
url: https://preview.aclanthology.org/fix_video/P16-1174.pdf
fetched: 2026-11-15（網頁讀取工具）
coverage: 全文
quote_verified: yes
---

## 驗證過的原文（1 句）
"improve Duolingo daily student engagement by 12% in an operational user study"

## 擷取重點（改寫，非原文）
- 半衰期回歸（half-life regression, HLR）：記得的機率隨時間下降，下降速度看這個字在你腦中的「半衰期」；每次成功練習，半衰期變長。公式 p = 2^(−Δ/h)。
- 用約 1,290 萬筆 Duolingo 練習紀錄評估；預測誤差比 Leitner 法低約 45%、比 Pimsleur 法低約 71%。
- 上線實驗：摘要稱每日學生活躍度提升 12%。細節：這是實驗 II 中兩個 HLR 版本的比較，不是 HLR 對傳統方法；實驗 I（HLR 對 Leitner）練習次數反而顯著下降 7.3%。
- 模型發現較難記的字：不規則變化、罕用字、過去式變化（例：德文 war）；較好記的：同源字、常見簡單字（例：Baby、camera）。
