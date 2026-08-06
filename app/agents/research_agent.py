
from app.rag.retriever import search_knowledge_base
from app.agents.state import OrbitalOpsState,ResearchFindings,RetrievedDocument



def research_node(state: OrbitalOpsState) -> OrbitalOpsState:
    anomalous_params =state.anomaly_info.anomalous_parameters

    query = "anomalous involving " + ", ".join(anomalous_params)

    results = search_knowledge_base(query, top_k=5)

    retrieved_docs = []

    for doc , score in results:
        retrieved_docs.append(
            RetrievedDocument(
                source_file=doc.metadata['source_file'],
                document_type=doc.metadata['document_type'],
                content_snippet=doc.page_content,
                similarity_score=score ,
            )

        )

    state.research_findings = ResearchFindings(
        retrieved_documents=retrieved_docs,
        query_used=query,
        total_documents_found=len(retrieved_docs)
    )

    return state

    




