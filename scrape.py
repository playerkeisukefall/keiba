import sys
import requests
import time
import csv
from bs4 import BeautifulSoup
import urllib3
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

RACE_RESULT_SAVE_DIR = "./raceResultCsv/"
REFUND_SAVE_DIR = "./refundCsv/"
BASE_URL = "https://db.netkeiba.com/race/"

args = sys.argv

def writeToCsv(csvTable, path):
    with open(path, "w") as f:
        csv.writer(f).writerows(csvTable)

def scrapeRefund(tables):
    csvTable = []
    for i in range(len(tables)):
        lines = tables[i].select("tr")
        for j in range(len(lines)):
            betType = lines[j].find("th").getText()
            cells = lines[j].select("td")
            if betType == "複勝" or betType == "ワイド":
                nArray = cells[0].getText(".").split(".")
                rArray = cells[1].getText(".").split(".")
                for k in range(len(nArray)):
                    csvTable.append([betType, nArray[k], rArray[k]])
            else:
                n = cells[0].getText()
                r = cells[1].getText()
                csvTable.append([betType, n, r])
    return csvTable


def scrapeRaceResult(table):
    csvTable = []
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
            csvTable.append(csvArray)
    return csvTable

def main():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1,  status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    year = int(args[1])
    for i in range(1, 11):
        for j in range(1, 11):
            for k in range(1, 11):
                for l in range(1, 13):
                    raceId = str(year) + str(i).zfill(2) + str(j).zfill(2) + str(k).zfill(2) + str(l).zfill(2)
                    url = BASE_URL + raceId
                    res = session.get(url=url, stream=True, timeout=(10.0, 30.0))
                    res.encoding = res.apparent_encoding
                    soup = BeautifulSoup(res.text, "html.parser")
                    raceResultTable = soup.select("table[summary=\"レース結果\"]")
                    refundTables = soup.select("table[summary=\"払い戻し\"]")
                    if raceResultTable:
                        raceResultTable = scrapeRaceResult(raceResultTable[0])
                        refundTable = scrapeRefund(refundTables)
                        writeToCsv(raceResultTable, RACE_RESULT_SAVE_DIR + raceId + ".csv")
                        writeToCsv(refundTable, REFUND_SAVE_DIR + raceId + ".csv")
                        print("raceId: %s - ok" % raceId)
                    else:
                        print("raceId: %s - not exist" % raceId)

if __name__ == '__main__':
    main()
