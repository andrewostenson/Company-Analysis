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
    
def get_lastest_10K(filing_history):
    recent = filing_history['filings']['recent']
    forms = recent['form']
    accession_numbers = recent['accessionNumber']
    filing_dates = recent['filingDate']
    primary_documents = recent['primaryDocument']

    for index, form in enumerate(forms):
        if form == '10-K':
            return {
                'accession_number': accession_numbers[index],
                'filing_date': filing_dates[index],
                'primary_document': primary_documents[index]
            }
    return None

def get_10K_document(cik, accession_number, primary_document):
    accession_number_no_dashes = accession_number.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_number_no_dashes}/{primary_document}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None 

if __name__ == '__main__':
    ticker = input("Enter a stock ticker: ")
    cik = get_cik(ticker)
    if cik:
        print(f"CIK for {ticker}: {cik}")
        filing_history = get_filing_history(cik)
        recent_10K = get_lastest_10K(filing_history)
        if recent_10K:
            document = get_10K_document(cik, recent_10K['accession_number'], recent_10K['primary_document'])
            if document:
                with open("data/10K_document.json", "w", encoding="utf-8") as file:
                    json.dump(document, file, indent=4)
        else:
            print(f"Could not retrieve latest 10-K for CIK {cik}.")
    else:
        print(f"No CIK found for ticker {ticker}.")