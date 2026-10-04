# SEC 10-K Analysis
A document analysis application that retrieves SEC 10-K filings, process and chunks the contents, generates semantic embeddings, and stores the resulting representations in a vector database. Users can then query a company's filing and fetch the most relevant sections for analysis.

## Overview
I built this project to explore how to process large financial documents and search them using modern-day NLP and LLM techniques. SEC 10-K filings can be long and dense documents about a companies financial performance, risks, business operations, and strategy. Finding this informaiton manually can be time consuming, especially when comparing multiple companies to each other. This application uses SEC filings as source data to cut down manual search time and identify the most relevant sections of the document, based on the user's query.

## Features
- Retrieves company 10-K filings using SEC EDGAR
- Processes and cleans documents for analysis
- Splits large filings into smaller, overlapping text chunks to retain context
- Generates semantic embeddings using Sentence Transformers
- Stores document embeddings in a persistent ChromaDB vector database
- Performs similarity-based retrieval to find the most relevant document sections
- Runs on an Oracle Cloud VM for persistant storage and public access

## Architecture
The pipeline follows this general workflow: 
**SEC 10-K -> Document processing -> Chunking -> Embeddings -> ChromaDB -> Similarity-based Search -> LLM Analysis**
1. A company ticker is selected in the application
2. The application retrieves the selected company's lastest 10-K filing using edgartools
3. The filing is processed into smaller chunks
4. Each chunk is converted into a semantic embedding using the all-MiniLM-L6-v2 transformer
5. The embeddings and associated chunks are stored within the persistent ChromaDB
6. When a user enters a query, the query is converted into an embedding with the same model
7. ChromaDB compares the query embedding against the stored document embeddings and returns the matching sections
8. The matching sections are then used to provide context to the LLM in order to generate a relevant response

## Technologies
- **Python** - Document processing and logic
- **edgartools** - SEC retrieval and processing
- **Sentence Transformers** - Calculation of text embeddings
- **all-MiniLM-L6-v2** - Embedding model used for documents and queries
- **ChromaDB** - Vector database used for persistent data storage and similarity search
- **Oracle Cloud** - Cloud VM used to host the application and database
- **Git** - Version control and management


## Demo
http://129.146.53.178:8501/

## Future Improvements
Going forward I'd like to improve model response, as well as add more filings for the application to source data from (e.g. SEC N-CSR's or Form 4's). I would also like to add data visualization to the application response.