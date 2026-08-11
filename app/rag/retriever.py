
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os
from app.core.constants import COLLECTION_NAME


def get_vector_store():
    client= QdrantClient(
        url = os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return QdrantVectorStore(
        client = client ,
        collection_name = COLLECTION_NAME ,
        embedding = embeddings
    )


def search_knowledge_base(query:str, top_k: int=5):
    vector_store = get_vector_store()
    return vector_store.similarity_search_with_score(query,k=top_k)


def format_evidence(retrieved_docs):
    pieces = []
    for doc in retrieved_docs:
        pieces.append(f"[Source: {doc.source_file}]\n{doc.content_snippet}")
    return "\n\n".join(pieces)



