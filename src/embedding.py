import sec_ret as sec
from sentence_transformers import SentenceTransformer

def embedChunks(chunks):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)
    return embeddings

def embed10K():
    document = sec.get_lastest_10K()
    chunks = sec.chunk_10K(document)
    text = [doc.page_content for doc in chunks]
    embeddings = embedChunks(text)
    return embeddings