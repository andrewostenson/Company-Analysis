import chromadb
import embedding as em
import sec_ret as sec

chroma_client = chromadb.PersistentClient(path="/home/ubuntu/Company-Analysis/chroma_data")
collection = chroma_client.get_or_create_collection(name="secAnalysis")
model = em.intModel()

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
    print(results)
    return results

if __name__ == "__main__":
    q = input("Enter query")
    buildCollection()
    embeddedq = em.embedUserInput(q, model)
    queryCollection(embeddedq)