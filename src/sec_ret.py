from edgar import *
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from transformers import AutoTokenizer

set_identity("ostensonandrew@gmail.com")

def get_lastest_10K():
    while True:
        try:
            company_request = input("Enter a stock ticker: ")
            filing = (Company(company_request)).get_filings(form="10-K")[0]
            filing_txt = filing.markdown() #C onvert 10K into markdown for chunking

            try:
                with open('data/10K-doc.txt', 'w') as file:
                    file.write(filing_txt)

                print(f"Saved latest 10-K for {company_request} to data/10K-doc.txt")
                return filing_txt


            except OSError as e:
                print(f"10K file could not be written: {e}")

        except NotFoundError as e:
            print(f"No such company: {e}")
            continue

def chunk_10K(markdown_document):
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2") # Chunk based on token size of model
    headers_to_split_on = [ 
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    # Split on headers
    markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on, strip_headers=False
)
    md_header_splits = markdown_splitter.split_text(markdown_document)

    # Create chunks 
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer, chunk_size=100, chunk_overlap=10
    )

    # Finalize chunks with respect to markdown headers and tokens
    splits = text_splitter.split_documents(md_header_splits)
    return splits

    
if __name__ == '__main__':
    document = get_lastest_10K()
    chunks = str(chunk_10K(document))

    with open('data/chunked10K.txt', 'w') as file:
        file.write(chunks)