# 間隔重複 App 怎麼替你排複習（SRS 演算法）

## 白話版
Anki、Duolingo 這類 App 會猜「你什麼時候快忘記這個字」，在那之前叫你複習。
每次你答對，下次複習就排得更遠。

## 研究怎麼說
- Duolingo 的模型把每個字想成有「記憶半衰期」；每成功練習一次，半衰期就變長。[[cards/settles2016#settles2016-1]]
- 用約 1,290 萬筆練習紀錄測試，預測誤差比 Leitner 排程法低約 45%。[[cards/settles2016#settles2016-2]]
- 模型也發現哪些字比較難：不規則變化、罕用字（例如德文 war）。[[cards/settles2016#settles2016-4]]

## 小心解讀
- 論文摘要說活躍度提升 12%，但那是兩個模型版本互比，不是「用 App 比不用好 12%」；另一組實驗中練習次數反而下降 7.3%。[[cards/settles2016#settles2016-3]]

## 相關
- [[concepts/spaced-practice]]
