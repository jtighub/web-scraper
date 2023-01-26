from bs4 import BeautifulSoup as soup
import requests
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

# web scraping Yahoo Finance for historical share value

ticker_dict = {}

ticker_inp = "AMZN" #input("Ticker: ").upper()
YAHOO_URL = f"https://finance.yahoo.com/quote/{ticker_inp}/history?period1=1513555200&period2=1671321600&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"

#f"https://uk.finance.com/quote/{ticker_inp}/history?period1=345427200&period=1660780800&interval=1mo&filter=history&frequency=1d&includeAdjustedClose=true"

html = requests.get(YAHOO_URL, headers={"User-Agent": "Mozilla/5.0"}).content.decode("utf-8")
htmlsoup = soup(html, features="html.parser")

# get ticker info
ticker_full = htmlsoup.find_all("h1", {"class": "D(ib)"})[0].get_text()
print(ticker_full)
ticker_caps = ticker_full[ticker_full.find("(")+1:ticker_full.find(")")]
ticker_org = ticker_full[:ticker_full.find("(")-1]

# get share price info as html (between td tags)
tds = htmlsoup.find_all("td", {"class": "Py(10px)"})

data = []
dividends = []
stock_split = []

# get share price info as text and insert into data as list
for td in tds:
    data += [td.get_text()]

for i in data[::1]:
    if "Dividend" in i:
        dividend_index = data.index(i)
        dividends.append(((data[dividend_index-1]), (data[dividend_index])))
        del data[dividend_index], data[dividend_index-1]
    elif "Stock split" in i:
        stock_split_index = data.index(i)
        stock_split.append(((data[stock_split_index-1]),(data[stock_split_index])))
        del data[stock_split_index], data[stock_split_index-1]


#print(data)
dates =[]
open_val = []
high_val = []
low_val = []
close_val = []
close_val_adj = []
volume = []

# values is list of lists
values = [dates, open_val, high_val, low_val, close_val, close_val_adj, volume]
# values_tup is a list of tuples
values_tup = []

for n in range(1, 100):
    a = (*data[7*n-7:7*n],)
    values_tup.append(a)

print(values_tup)
# get data from table of 7 columns

for n in range(7):
    # for dates(str)
    if n == 0:
        for i in data [n::7]:
            values[n].append(i)
    # for values (float)
    else:
        for i in data [n::7]:
            # remove comma separators and convert from str to float
            values[n].append(float(i.replace(",","")))

if stock_split: print("Stock splits: ", stock_split)
if dividends: print("Dividents: ", dividends)

print(len(close_val))
# store data in sql3 database
con = sqlite3.connect("tracking_service/historic_share_prices.db")
cur = con.cursor()
cur.execute(f"DROP TABLE IF EXISTS {ticker_caps}")


share_price_details = f"""
    CREATE TABLE IF NOT EXISTS {ticker_caps} (
        dates TEXT,
        open_val TEXT,
        high_val TEXT,
        low_val TEXT,
        close_val TEXT,
        close_val_adj TEXT,
        volume TEXT
        )"""

cur.execute(share_price_details)

for line in values_tup:
    cur.execute(f"INSERT INTO {ticker_caps} VALUES(?, ?, ?, ?, ?, ?, ?)", line)

con.commit()

a = input("Check if table is in database: ")
s = f"SELECT * FROM {a.upper()}"
cur.execute(s)
results = cur.fetchall()
print(a.upper(), "Hisotrical Data: ", results)
con.close()

# reversed list data to plot dates in forward direction
plt.plot(np.array(dates[::-1]), np.array(close_val[::-1]))
plt.xlabel("Date")
plt.ylabel("Price in USD")
plt.title(f"{ticker_full} Share Price")
plt.show()