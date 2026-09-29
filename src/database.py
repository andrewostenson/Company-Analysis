import chromadb
import sec_ret as sec
from openai import OpenAI

chroma_client = chromadb.PersistentClient(path="/app/chroma_data")
collection = chroma_client.get_or_create_collection(name="secAnalysis")
model = sec.initModel()
client = OpenAI()

def buildCollection(ticker):
    chunks = sec.getChunks(ticker)

    metadata = sec.getMetadata(chunks)
    documents = sec.getPageContent(chunks)
    embeddings = sec.embedPageContent(documents, model)
    doc_ids = [str(x) for x in range(len(documents))]

    collection.add(ids = doc_ids, embeddings = embeddings, metadatas = metadata, documents = documents)

def queryCollection(embeddings):
    results = collection.query(
        query_embeddings = embeddings
    )
    return results

def embedQuestion(question):
    embedding = sec.embedUserInput(question, model)
    return embedding

def gptQuery(query, chunks):
    documents = chunks["documents"][0]
    context = "\n\n".join(documents)

    gpt_input = f"""
    Use the following SEC input to answer the question.

    Context:
    {context}

    Question:
    {query}
    """

    response = client.responses.create(
    model="gpt-5-mini",
    input=gpt_input
    )
    return response.output_text