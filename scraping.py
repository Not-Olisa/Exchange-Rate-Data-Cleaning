import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timezone
import time


#creating a variable to store the website url

url = "https://www.x-rates.com/table/?from=USD&amount=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  "AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/120.0.0.0 Safari/537.36"
}

#sending a GET request to the webpage using the url variable.

response = requests.get(url, headers=headers)
response.raise_for_status()

#parse html using beautiful soup
soup = BeautifulSoup(response.text, "lxml")

#Find the table where data is located. could not be table in other cases.
table = soup.find("table", {"class":"tablesorter ratesTable"})

#extract column headers
headers = []
for th in table.find_all("th"):
    headers.append(th.text.strip())

print("Headers found:", headers)

#Extract table rows
rows = []
for tr in table.find_all("tr")[1:]:  # skip the first row (headers)
    cells = [td.text.strip() for td in tr.find_all("td")]
    if cells:  # only keep non-empty rows
        rows.append(cells)

#Convert to DataFrame
df = pd.DataFrame(rows, columns=headers)

#Add timestamp column. optional but for analysis justt= add for documentation.
df["scrape_utc"] = datetime.now(timezone.utc).isoformat()

#Save as CSV
df.to_csv("exchange_rates_bs.csv", index=False, encoding="utf-8")
print("Saved exchange_rates_bs.csv")
print(df.head())



