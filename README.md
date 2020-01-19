# 【python】【競馬】結局、最強の賭け方はなんなのか？

# 実行環境
- MacOs Sierra 10.12.6
- anaconda3-5.2.0（Python 3.6.5）

# 実行手順
## 1. csv を格納するディレクトリを用意
scrape.py で
- raceResultCsv: レース結果
- refundCsv: 払い戻し

という 2 つのディレクトリに csv を格納するので、ディレクトリを用意する
```
mkdir raceResultCsv
mkdir refundCsv
```

## 2. スクレイピング
https://db.netkeiba.com からレース情報からスクレイピングを行う
```
python runScraping.py
```

#### ●説明
- 2008年 ~ 2019年のデータを年ごとに並列でスクレイピングする
- 実際に動いているのは ```scrape.py``` で、```runScraping.py``` は並列でバックグラウンド実行させるスクリプト

#### ●処理が終わったかどうか
```
ps aux | grep scrape.py
```

みたいな感じで適当にプロセスを確認して 11 個のプロセスが全部なくなっていたらスクレイピング終了

## 3. シミュレーション
全てのレース結果を使ってシミュレーションを行う
```
python simulate.py
```

#### ●出力
```
simulate now ... xxx / 37196 [race]
```

#### ●結果
result.csv にシミュレーション結果が書き出される
