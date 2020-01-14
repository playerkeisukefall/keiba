import requests
import csv
from bs4 import BeautifulSoup

CSV_SAVE_DIR = "./csvData/"
BASE_URL = "https://db.netkeiba.com/race/"

def writeToCsv(csv2dArray, path):
    with open(path, "w") as f:
        csv.writer(f).writerows(csv2dArray)

def scrape(table):
    csv2dArray = []
    lines = table.select("tr")
    for i in range(len(lines)):
        if i != 0: # ヘッダーはパスする
            csvArray = []
            cells = lines[i].select("td")
            csvArray.append(cells[0].getText()) # 着順
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
                        res.encoding = res.apparent_encoding
                        soup = BeautifulSoup(res.text, "html.parser")
                        raceTable = soup.select("table[summary=\"レース結果\"]")
                        if raceTable: # レースが存在しない場合パスする
                            csv2dArray = scrape(raceTable[0])
                            writeToCsv(csv2dArray, CSV_SAVE_DIR + raceId + ".csv")
                            print("raceId: %s - ok" % raceId)

if __name__ == '__main__':
    main()
