import requests
import time
import csv
from bs4 import BeautifulSoup

RACE_RESULT_SAVE_DIR = "./raceResultCsv/"
REFUND_SAVE_DIR = "./refundCsv/"
BASE_URL = "https://db.netkeiba.com/race/"

def writeToCsv(csv2dArray, path):
    with open(path, "w") as f:
        csv.writer(f).writerows(csv2dArray)

def scrapeRefund(tables):
    csv2dArray = []
    for i in range(len(tables)):
        lines = tables[i].select("tr")
        for j in range(len(lines)):
            betType = lines[j].find("th").getText()
            cells = lines[j].select("td")
            if betType == "複勝" or betType == "ワイド":
                n1, n2, n3 = cells[0].getText(".").split(".")
                r1, r2, r3 = cells[1].getText(".").split(".")
                csv2dArray.append([betType, n1, r1])
                csv2dArray.append([betType, n2, r2])
                csv2dArray.append([betType, n3, r3])
            else:
                n = cells[0].getText()
                r = cells[1].getText()
                csv2dArray.append([betType, n, r])
    return csv2dArray


def scrapeRaceResult(table):
    csv2dArray = []
    lines = table.select("tr")
    for i in range(len(lines)):
        if i != 0: # ヘッダーはパスする
            csvArray = []
            cells = lines[i].select("td")
            csvArray.append(cells[0].getText()) # 着順
            csvArray.append(cells[1].find("span").getText()) # 枠番
            csvArray.append(cells[2].getText()) # 馬番
            csvArray.append(cells[12].getText()) # オッズ
            csvArray.append(cells[13].getText()) # 人気
            csv2dArray.append(csvArray)
    return csv2dArray

def main():
    for year in range(2008, 2009):
        for i in range(1, 11):
            for j in range(1, 11):
                for k in range(1, 11):
                    for l in range(1, 13):
                        raceId = str(year) + str(i).zfill(2) + str(j).zfill(2) + str(k).zfill(2) + str(l).zfill(2)
                        url = BASE_URL + raceId
                        res = requests.get(url)
                        time.sleep(0.5)
                        res.encoding = res.apparent_encoding
                        soup = BeautifulSoup(res.text, "html.parser")
                        raceResultTable = soup.select("table[summary=\"レース結果\"]")
                        refundTables = soup.select("table[summary=\"払い戻し\"]")
                        if raceResultTable: # レースが存在しない場合パスする
                            raceResult2dArray = scrapeRaceResult(raceResultTable[0])
                            refund2dArray = scrapeRefund(refundTables)
                            writeToCsv(raceResult2dArray, RACE_RESULT_SAVE_DIR + raceId + ".csv")
                            writeToCsv(refund2dArray, REFUND_SAVE_DIR + raceId + ".csv")
                            print("raceId: %s - ok" % raceId)

if __name__ == '__main__':
    main()
