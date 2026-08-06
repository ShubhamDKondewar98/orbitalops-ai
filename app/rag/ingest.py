
from pathlib import Path 
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os 
from dotenv import load_dotenv
load_dotenv()



from app.core.constants import CHUNK_OVERLAP, CHUNK_SIZE


KNOWLEDGE_BASE_PATH = Path("knowledge_base")   # folder name where data lies 

FOLDER_TO_DOCUMENT_TYPE = {
    "incident-reports": "incident_report",
    "operational-procedures": "operational_procedure",
    "mission-knowledge": "mission_knowledge",
}


def load_knowledge_base():
    docs  = []

    for folder_name , doc_type in FOLDER_TO_DOCUMENT_TYPE.items():
        folder_path = KNOWLEDGE_BASE_PATH / folder_name

        for file_path in folder_path.glob("*.txt"):
            text = file_path.read_text(encoding="utf-8")

            doc = Document(
                page_content=text,
                metadata={
                    "source_file": file_path.name,
                    "document_type": doc_type,
                },
            )
            docs.append(doc) 

    return docs   


def split_into_chunks(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    return splitter.split_documents(docs)



COLLECTION_NAME = "aether1_knowledge"

def upload_to_qdrant(chunks):
    client = QdrantClient(
        url = os.getenv("QDRANT_URL"),
        api_key = os.getenv("QDRANT_API_KEY"),
    )

    embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")

    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name = COLLECTION_NAME ,
        vectors_config = VectorParams(
            size = 1536,
            distance = Distance.COSINE
        )
    )

    vector_store = QdrantVectorStore(
        client = client ,
        collection_name = COLLECTION_NAME ,
        embedding = embeddings ,
    )

    vector_store.add_documents(chunks)

    print(f"Uploaded {len(chunks)} chunks to Qdrant collection '{COLLECTION_NAME}'")



if __name__ == "__main__":
    docs = load_knowledge_base()
    chunks = split_into_chunks(docs)
    upload_to_qdrant(chunks)




        



