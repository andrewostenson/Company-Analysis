import json
import requests

headers = {'User-Agent': "Andrew Ostenson ostensonandrew@gmail.com"}

with open('data/company_tickers.json') as r:
    tickers = json.load(r)

def get_cik(ticker):
    ticker = ticker.upper()
    for company in tickers.values(): # Iterate through each company in the tickers dictionary
        if company['ticker'] == ticker:
            return str(company['cik_str']).zfill(10) # Pad the CIK with leading zeros to ensure it is 10 digits long
    return None

def get_filing_history(cik):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json" # Construct the URL to fetch the filing history for the given CIK
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_lastest_10K(filing_history):
    recent = filing_history['filings']['recent'] # Access the 'recent' filings from the filing history
    forms = recent['form'] # Access the 'form' field from the recent filings, which contains the types of filings (e.g., 10-K, 10-Q, etc.)
    accession_numbers = recent['accessionNumber'] # Access the 'accessionNumber' field from the recent filings, which contains the unique identifiers for each filing
    filing_dates = recent['filingDate'] # Access the 'filingDate' field from the recent filings, which contains the dates of each filing
    primary_documents = recent['primaryDocument'] # Access the 'primaryDocument' field from the recent filings, which contains the names of the primary documents for each filing

    for index, form in enumerate(forms): # Iterate through the forms and their corresponding indices
        if form == '10-K':
            return {
                'accession_number': accession_numbers[index],
                'filing_date': filing_dates[index],
                'primary_document': primary_documents[index]
            }
    return None

def get_10K_document(cik, accession_number, primary_document):
    accession_number_no_dashes = accession_number.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_number_no_dashes}/{primary_document}" # Construct the URL to fetch the 10-K document using the CIK, accession number (without dashes), and primary document name
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
                with open("data/10K_document.html", "w", encoding="utf-8") as file:
                    file.write(document)
            else:
                print(f"Could not retrieve the 10-K document for CIK {cik}.")
        else:
            print(f"Could not retrieve latest 10-K for CIK {cik}.")
    else:
        print(f"No CIK found for ticker {ticker}.")