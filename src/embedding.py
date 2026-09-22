import sec_ret as sec
from sentence_transformers import SentenceTransformer

def embedChunks(chunks):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)
    return embeddings

def embedPageContent(pageContent):
    embeddings = embedChunks(pageContent)
    return embeddings