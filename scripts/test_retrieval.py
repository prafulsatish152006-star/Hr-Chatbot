import chromadb
from sentence_transformers import SentenceTransformer

client=chromadb.PersistentClient(
    path=r"C:\Users\prafu\Desktop\project-hr\chroma_db"
)

collection= client.get_collection(
    name="hr_knowledge"
)

print("Documents in database: ",collection.count())

model=SentenceTransformer("all-MiniLM-L6-v2")

question=input("Enter the HR question: ")

question_embedding= model.encode(question)

result= collection.query(
    query_embeddings=[question_embedding.tolist()],
    n_results=5
)

print("\n==============================")
print("RETRIEVAL RESULTS")
print("==============================")

for i in range(len(result["documents"][0])):
    print(f"\n--- Result {i + 1} ---")

    print("ID:", result["ids"][0][i])

    print("Distance:", result["distances"][0][i])

    print("\nDocument:")
    print(result["documents"][0][i])

    print("\nMetadata:")
    print(result["metadatas"][0][i])