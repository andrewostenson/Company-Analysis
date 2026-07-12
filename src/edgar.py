import json

with open('data/company_tickers.json') as r:
    tickers = json.load(r)

def get_cik(ticker):
    ticker = ticker.upper()

    for company in tickers.values():
        if company['ticker'] == ticker:
            return str(company['cik_str']).zfill(10)
    return None

if __name__ == '__main__':
    ticker = input("Enter a stock ticker: ")
    cik = get_cik(ticker)
    if cik:
        print(f"The CIK for {ticker} is {cik}.")
    else:
        print(f"No CIK found for {ticker}.")