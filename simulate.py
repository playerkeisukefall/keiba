import glob
import csv

CSV_SAVE_DIR = "./csvData/"
BET = 100

def getRefund(csvData):
    if csvData[0][2] == "1":
        return int(round(BET * float(csvData[0][1]), -1))
    else:
        return 0

def main():
    balance = 0

    csvList = glob.glob(CSV_SAVE_DIR + "*")
    for csvPath in csvList:
        with open(csvPath) as f:
            csvData = [row for row in csv.reader(f)] # csv を 2 次元配列として取得
            balance -= BET
            balance += getRefund(csvData)
            print("{:,}".format(balance))

if __name__ == '__main__':
    main()
