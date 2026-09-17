import json
import requests
from bs4 import BeautifulSoup
import re

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
    
def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser') 
    pattern = r"(Item\s+\d+[A-Z]?\.)" # Regex pattern to match "Item" followed by a number and an optional letter, ending with a period
    full_text = soup.get_text(strip=True, separator='\n') # Extract all text from the HTML content, stripping leading and trailing whitespace
    parts = re.split(pattern, full_text) # Split the text into parts based on the regex pattern
    sections = []

    for i in range(1, len(parts), 2): # Iterate through the parts, starting from index 1 and stepping by 2 to get the "Item" sections
        item_label = parts[i] # The "Item" label (e.g., "Item 1.")
        item_content = parts[i + 1] if i + 1 < len(parts) else "" # The content corresponding to the "Item" label, or an empty string if there is no content
        sections.append({
            "item": item_label,
            "content": item_content.strip()
        })

    best_by_item = {}
    for section in sections:
        label = section["item"]
        if label not in best_by_item:
            best_by_item[label] = section
        elif len(section["content"]) > len(best_by_item[label]["content"]):
            best_by_item[label] = section

    filtered_sections = list(best_by_item.values())
    print("Number of sections extracted:", len(filtered_sections)) # Print the number of sections extracted
    return filtered_sections
    
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
                cleaned_sections = clean_html(document)
                with open(f"data/10K_document.txt", "w", encoding="utf-8") as f:
                    for section in cleaned_sections:
                        f.write(f"{section['item']}\n{section['content']}\n\n")
                print(f"Successfully retrieved and cleaned the 10-K document for CIK {cik}.")
            else:
                print(f"Could not retrieve the 10-K document for CIK {cik}.")
        else:
            print(f"Could not retrieve latest 10-K for CIK {cik}.")
    else:
        print(f"No CIK found for ticker {ticker}.")