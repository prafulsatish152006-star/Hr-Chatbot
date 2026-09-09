from docx import Document 
import re 
import json


#loading the hr policy which we have stored
policy_path = r"C:\Users\prafu\Desktop\project-hr\documents\hr policies.docx"

doc=Document(policy_path)

print("HR document successfully loaded")

#extracting text

paragraphs= []

for paragraph in doc.paragraphs:

    text=paragraph.text.strip()

    if text:
        paragraphs.append(text)


print("paragraph extracted: ",len(paragraphs))

policy_text= "\n".join(paragraphs)

#both the next 2 lines are for cleaning 
#first line is for making multiple blank lines into single line without any blanks
policy_text = re.sub(r"\n+", "\n", policy_text)
#multiple spaces with single normal space
policy_text =re.sub(r"[ \t]+", " ",policy_text)

policy_text=policy_text.strip()

print("Total policy Characters: ",len(policy_text))

#Chunking process

chunk_size=1500
chunk_overlap=200

policy_chunk=[]

start=0

while start<len(policy_text):

    end=start+chunk_size

    chunk=policy_text[start:end].strip()

    if chunk:
        policy_chunk.append(chunk)

    start=end-chunk_overlap

print("Total policy chunks: ",len(policy_chunk))

#creating ids and metadatas

policy_data=[]

for i,chunk in enumerate(policy_chunk):

    policy_data.append({

        "id": f"policy_{i}",

        "text": chunk,

        "metadata":{
            "source_type":"policy",
            "document": "HR policy",
            "chunk_number": i
        }
    })

print("\n------------THE FIRST POLICY CHUNK------------\n")

print(policy_data[0]["text"])

#Saving chunks

output_path= r"C:\Users\prafu\Desktop\project-hr\documents\hr_policy_chunks.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(
        policy_data,
        file,
        indent=2,
        ensure_ascii=False
    )

print("\n===================================")
print("POLICY PROCESSING COMPLETED")
print("===================================")

print("Policy chunks:", len(policy_data))

print("Saved to:")
print(output_path)