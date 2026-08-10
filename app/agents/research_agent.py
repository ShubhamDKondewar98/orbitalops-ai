
from app.rag.retriever import search_knowledge_base
from app.agents.state import OrbitalOpsState,ResearchFindings,RetrievedDocument
from app.core.logging_config import get_logger
logger = get_logger(__name__)

MAX_RETRIES = 2


def research_node(state: OrbitalOpsState) -> OrbitalOpsState:
    anomalous_params =state.anomaly_info.anomalous_parameters

    query = "anomalous involving " + ", ".join(anomalous_params)

    attempt = 0
    while attempt <= MAX_RETRIES:
        try:
            print(f"query for retriving data {query} ")

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

            print(f"retrived documents are: {retrieved_docs}")

            state.research_findings = ResearchFindings(
                retrieved_documents=retrieved_docs,
                query_used=query,
                total_documents_found=len(retrieved_docs)
            )
            logger.info(f"Research completed, found {len(retrieved_docs)} documents")
            return state

        except Exception as e:
            attempt += 1
            logger.warning(f"Research attempt {attempt} failed: {e}")
            state.retry_counts["research"] = attempt

    logger.error("Research failed after all retries, marking pipeline degraded")
    state.pipeline_status = "degraded"
    state.failed_stages.append("research")
    state.research_findings = ResearchFindings(
        retrieved_documents=[],
        query_used=query,
        total_documents_found=0,
    )
    return state

    




