
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import OrbitalOpsState,RootCauseAnalysis
from app.rag.retriever import format_evidence
from app.core.logging_config import get_logger
logger = get_logger(__name__)



llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
structured_llm = llm.with_structured_output(RootCauseAnalysis)

rca_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a spacecraft systems engineer investigating an anomaly on AETHER-1. "
               "Use ONLY the provided evidence to determine possible causes. "
               "Do not invent information not present in the evidence. "
               "If the evidence is weak or doesn't clearly explain the anomaly, "
               "reflect that with a low confidence score.") ,

    ("human", "Anomalous parameters: {anomalous_parameters}\n"
              "Severity: {severity}\n"
              "Correlated parameters checked: {correlated_parameters}\n\n"
              "Retrieved evidence:\n{evidence}\n\n"
              "Based on this evidence, identify possible root causes with confidence scores."),

])


rca_chain =  rca_prompt | structured_llm  


MAX_RETRIES = 2


def root_cause_analysis_node(state: OrbitalOpsState) -> OrbitalOpsState:
    anomaly = state.anomaly_info
    evidence = format_evidence(state.research_findings.retrieved_documents)

    attempt = 0
    while attempt <= MAX_RETRIES:
        try:
            result = rca_chain.invoke({
                "anomalous_parameters": ", ".join(anomaly.anomalous_parameters),
                "severity": anomaly.severity,
                "correlated_parameters": ", ".join(anomaly.correlated_parameters_checked),
                "evidence":  evidence ,
            }) 

            state.root_cause_analysis = result
            logger.info(f"RCA completed, confidence={result.overall_confidence}")
            return state

        except Exception as e:
            attempt += 1
            logger.warning(f"RCA attempt {attempt} failed: {e}")
            state.retry_counts["root_cause_analysis"] = attempt

    logger.error("RCA failed after all retries, marking pipeline degraded")
    state.pipeline_status = "degraded"
    state.failed_stages.append("root_cause_analysis")
    state.root_cause_analysis = RootCauseAnalysis(
        possible_causes=[],
        correlated_parameters=[],
        requires_human_review=True,
        overall_confidence=0.0,
    )
    return state











