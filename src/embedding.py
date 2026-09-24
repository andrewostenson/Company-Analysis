import sec_ret as sec
from sentence_transformers import SentenceTransformer

def intModel():
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return model;

def embedChunks(chunks, model):
    embeddings = model.encode(chunks)
    return embeddings

def embedPageContent(pageContent, model):
    embeddings = embedChunks(pageContent, model)
    return embeddings

def embedUserInput(uInput, model):
    embedding = model.encode(uInput)
    return embedding
