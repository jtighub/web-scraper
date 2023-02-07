# taken from web-scraper tracking service
import requests
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd

ticker_dict = {}

ticker_inp = "JPM"
YAHOO_URL = f"https://finance.yahoo.com/quote/{ticker_inp}/holders?p={ticker_inp}"

html = requests.get(YAHOO_URL, headers={"User-Agent": "Mozilla/5.0"}).content.decode("utf-8")
htmlsoup = BeautifulSoup(html, features="html.parser")

# scrape tables in html. Table at index [1] shows institutional holders
table = htmlsoup.find_all('table')
df = pd.read_html(str(table))[1]

print(df.tail())

# convert to node list (institutions) and edge list (directed, with % shares)?