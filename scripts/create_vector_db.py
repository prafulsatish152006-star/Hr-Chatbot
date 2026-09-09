import json 
import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd

employee_path = r"C:\Users\prafu\Desktop\project-hr\documents\employee_documents.json"

with open(employee_path, "r", encoding="utf-8") as file:
    employee_data=json.load(file)

print("Employee document loaded: ",len(employee_data))

policy_path = r"C:\Users\prafu\Desktop\project-hr\documents\hr_policy_chunks.json"

with open(policy_path, "r", encoding="utf-8") as file:
    policy_data=json.load(file)

print("Policy chunk loaded: ",len(policy_data))


#combining both policy and employee data
all_data=policy_data+employee_data

documents= [item["text"]for item in all_data]

ids= [item["id"] for item in all_data]

metadatas= [item["metadata"] for item in all_data]

print("total documents: ",len(documents))

#loading embelling model

print("Loading embelling model...")

model=SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded. ")

print("Creating embeddings...")

embeddings= model.encode(
    documents,
    show_progress_bar=True
)

print("Embedding created: ",len(embeddings))

print("Creating chromadb...")

client=chromadb.PersistentClient(
    path=r"C:\Users\prafu\Desktop\project-hr\chroma_db"
)

collection= client.get_or_create_collection(
    name="hr_knowledge"
)

print("storing documents...")

#upsert means update and insert
collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas

)

print("VECTOR DATABASE CREATED")
print("==============================")

print("Employee records:", len(employee_data))
print("Policy chunks:", len(policy_data))
print("Total records:", collection.count())