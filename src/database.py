import chromadb
import embedding as em
import sec_ret as sec
from openai import OpenAI

chroma_client = chromadb.PersistentClient(path="/home/ubuntu/Company-Analysis/chroma_data")
collection = chroma_client.get_or_create_collection(name="secAnalysis")
model = em.intModel()
client = OpenAI()

def buildCollection():
    chunks = sec.getChunks()

    metadata = sec.getMetadata(chunks)
    documents = sec.getPageContent(chunks)
    embeddings = em.embedPageContent(documents, model)
    doc_ids = [str(x) for x in range(len(documents))]

    collection.add(ids = doc_ids, embeddings = embeddings, metadatas = metadata, documents = documents)

def queryCollection(embeddings):
    results = collection.query(
        query_embeddings = embeddings
    )
    return results

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
    print(response.output_text)

if __name__ == "__main__":
    q = input("Enter query")
    buildCollection()
    embeddedq = em.embedUserInput(q, model)
    collection = queryCollection(embeddedq)
    gptQuery(q, collection)