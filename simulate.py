import os
import sys
import glob
import csv

RACE_RESULT_SAVE_DIR = "./raceResultCsv/"
REFUND_SAVE_DIR = "./refundCsv/"
RESULT_SAVE_PATH = "result.csv"

def sortByBalance(table):
    table.sort(key=lambda x: x[4], reverse=True)

def checkBetType(betType, refundTable):
    for i in range(len(refundTable)):
        if betType == refundTable[i][0]:
            return True
    return False

def convertPopularityToHorseNum(popularityStr, raceResultTable):
    if " → " in popularityStr:
        exacta = True
        popularityStr = popularityStr.replace(" → ", ".", 2)
    else:
        exacta = False
        popularityStr = popularityStr.replace(" - ", ".", 2)
    popularityArray = popularityStr.split(".")
    horseNumArray = [-1] * len(popularityArray)
    for i in range(len(popularityArray)):
        for j in range(len(raceResultTable)):
            if popularityArray[i] == raceResultTable[j][4]:
                horseNumArray[i] = int(raceResultTable[j][2])
                break
    if -1 in horseNumArray:
        return "not exist"
    if not exacta:
        horseNumArray.sort()
    horseNumStr = ""
    for i in horseNumArray:
        horseNumStr += str(i)
        if exacta:
            horseNumStr += " → "
        else:
            horseNumStr += " - "
    horseNumStr = horseNumStr[0:-3]
    return(horseNumStr)

def simulate(resultTable, raceResultTable, refundTable):
    # resultTable から "賭ける馬の人気" を取り出す
    # "賭ける馬の人気" を "馬番" に変換
    for target in resultTable:
        betType = target[0]
        popularityStr = target[1]
        horseNumStr = convertPopularityToHorseNum(popularityStr, raceResultTable)
        if horseNumStr != "not exist" and checkBetType(betType, refundTable):
            target[2] += 1 # 試行回数 +1
            target[4] -= 100 # 収益 -100
            for i in range(len(refundTable)):
                if betType == refundTable[i][0] and horseNumStr == refundTable[i][1]:
                    target[3] += 1
                    target[4] += int(refundTable[i][2].replace(",", ""))
                    break

def initResultTable():
    maxRunningHorseNum = 18
    resultTable = [] # ["馬券タイプ", "賭ける馬の人気", "試行回数", "勝利回数", "収益"]　を格納する
    for i in range(1, maxRunningHorseNum + 1):
        resultTable.append(["単勝", str(i), 0, 0, 0])
        resultTable.append(["複勝", str(i), 0, 0, 0])
    for i in range(1, maxRunningHorseNum + 1):
        for j in range(i + 1, maxRunningHorseNum + 1):
            resultTable.append(["馬連", "%d - %d" % (i, j), 0, 0, 0])
            resultTable.append(["ワイド", "%d - %d" % (i, j), 0, 0, 0])
    for i in range(1, maxRunningHorseNum + 1):
        for j in range(1, maxRunningHorseNum + 1):
            if i != j:
                resultTable.append(["馬単", "%d → %d" % (i, j), 0, 0, 0])
    for i in range(1, maxRunningHorseNum + 1):
        for j in range(i + 1, maxRunningHorseNum + 1):
            for k in range(j + 1, maxRunningHorseNum + 1):
                resultTable.append(["三連複", "%d - %d - %d" % (i, j, k), 0, 0, 0])
    for i in range(1, maxRunningHorseNum + 1):
        for j in range(1, maxRunningHorseNum + 1):
            for k in range(1, maxRunningHorseNum + 1):
                if i != j and j != k and k != i:
                    resultTable.append(["三連単", "%d → %d → %d" % (i, j, k), 0, 0, 0])
    return resultTable

def main():
    resultTable = initResultTable() # シミュレーション結果を格納する配列を初期化
    csvList = glob.glob(RACE_RESULT_SAVE_DIR + "*")
    raceNum = len(csvList)
    raceCount = 1
    for csvPath in csvList:
        fileName = os.path.basename(csvPath)
        raceResultCsvPath = RACE_RESULT_SAVE_DIR + fileName
        refundCsvPath = REFUND_SAVE_DIR + fileName
        with open(raceResultCsvPath) as f:
            raceResultTable = [row for row in csv.reader(f)]
        with open(refundCsvPath) as f:
            refundTable = [row for row in csv.reader(f)]
        simulate(resultTable, raceResultTable, refundTable)
        sys.stdout.write("\r")
        sys.stdout.write("simulate now ... %d / %d [race]" % (raceCount, raceNum))
        sys.stdout.flush()
        raceCount += 1
        
    sortByBalance(resultTable)
    header = ["馬券タイプ", "賭ける馬の人気", "賭けた回数", "当たり回数", "収益"]
    resultTable.insert(0, header)
    with open(RESULT_SAVE_PATH, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(resultTable)

if __name__ == '__main__':
    main()
