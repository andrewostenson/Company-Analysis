from edgar import *

set_identity("ostensonandrew@gmail.com")

def get_lastest_10K():
    while True:
        try:
            company_request = input("Enter a stock ticker: ")
            filing = (Company(company_request)).get_filings(form="10-K")[0]
            filing_txt = filing.text()

            try:
                with open('data/10K-doc.txt', 'w') as file:
                    file.write(filing_txt)

                print(f"Saved latest 10-K for {company_request} to data/10K-doc.txt")
                break

            except OSError as e:
                print(f"10K file could not be written: {e}")

        except NotFoundError as e:
            print(f"No such company: {e}")
            continue


    
if __name__ == '__main__':
    get_lastest_10K()