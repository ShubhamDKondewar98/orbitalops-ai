
from pathlib import Path 
from langchain_community.document_loaders import DirectoryLoader , TextLoader

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
        loader = DirectoryLoader(
            str(folder_path), 
            glob="*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"})
        
        folder_docs = loader.load()

        for doc in folder_docs:
            doc.metadata = {
                "source_file": Path(doc.metadata["source"]).name,
                "document_type": doc_type,
            }

        docs.extend(folder_docs) 

    return docs      



        



