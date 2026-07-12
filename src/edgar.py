import json
import requests

headers = {'User-Agent': "Andrew Ostenson ostensonandrew@gmail.com"}

with open('data/company_tickers.json') as r:
    tickers = json.load(r)

def get_cik(ticker):
    ticker = ticker.upper()

    for company in tickers.values():
        if company['ticker'] == ticker:
            return str(company['cik_str']).zfill(10)
    return None

def get_filing_history(cik):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == '__main__':
    ticker = input("Enter a stock ticker: ")
    cik = get_cik(ticker)
    if cik:
        print(f"CIK for {ticker}: {cik}")
        filing_history = get_filing_history(cik)
        if filing_history:
            with open("data/test_data.json", "w", encoding="utf-8") as file:
                json.dump(filing_history, file, indent=4)
        else:
            print(f"Could not retrieve filing history for CIK {cik}.")
    else:
        print(f"No CIK found for ticker {ticker}.")