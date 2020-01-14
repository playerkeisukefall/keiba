# 【競馬】1番人気に賭け続けたら収益はどうなるのか

# 実行環境
- MacOs Sierra 10.12.6
- anaconda3-5.2.0（Python 3.6.5）

# 実行手順
## csv を格納するディレクトリを用意
scrape.py で
- raceResultCsv: レース結果
- refundCsv: 払い戻し

という 2 つのディレクトリに csv を格納するので、ディレクトリを用意する
```
mkdir raceResultCsv
mkdir refundCsv
```

## スクレイピング
https://db.netkeiba.com からレース情報からスクレイピングを行う
```
python scrape.py
```

実行結果
```
raceId: 200801010101 - ok
raceId: 200801010102 - ok
raceId: 200801010103 - ok
　　　　　　：
```
