import pickle
import time

import httpx
from bs4 import BeautifulSoup

with httpx.Client() as client:
    instruments = []
    start = 0
    while True:

        result = client.get("https://iss.moex.com/iss/securities", params={"group":"group", "group_by_filter":"stock_shares", "start":start})
        soup = BeautifulSoup(result.content, "lxml")
        res = soup.find_all("row")
        if not res:
            break
        for x in res:
            instruments.append((x.get("secid"), x.get("name"), x.get("group"))) 
        start += 100
        print(f"{res[-1].get("secid")=}, {start=}")
        time.sleep(0.03)

    with open("instruments.pikle", "wb") as f:
        pickle.dump(instruments, f)

    print(len(instruments))




