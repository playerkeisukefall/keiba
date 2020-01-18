import os

order = "nohup python scrape.py %s &"

for year in range(2008, 2019):
    os.system(order % (str(year)))
