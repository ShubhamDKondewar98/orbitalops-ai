
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import OrbitalOpsState,Recommendation
from app.rag.retriever import format_evidence
from app.core.logging_config import get_logger
logger = get_logger(__name__)


rec_llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
structured_rec_llm = rec_llm.with_structured_output(Recommendation)


rec_prompt = ChatPromptTemplate.from_messages([ 
    
    ("system", "You are a spacecraft systems engineer recommending actions for AETHER-1. "
               "Base your recommendations ONLY on the operational procedures provided in the evidence. "
               "Mark is_critical as true if the situation requires immediate human approval "
               "before action, based on the severity and root cause confidence."),

    ("human", "Severity: {severity}\n"
              "Root cause: {root_cause}\n"
              "RCA confidence: {rca_confidence}\n\n"
              "Retrieved evidence:\n{evidence}\n\n"
              "Recommend specific actions, grounded in the evidence above."), 

]) 

rec_chain = rec_prompt | structured_rec_llm 

MAX_RETRIES = 2

def recommendation_node(state: OrbitalOpsState) -> OrbitalOpsState:
    top_cause = state.root_cause_analysis.possible_causes[0]
    evidence = format_evidence(state.research_findings.retrieved_documents)

    attempt = 0
    while attempt <= MAX_RETRIES:
        try:
            result = rec_chain.invoke({
                "severity": state.anomaly_info.severity,
                "root_cause": top_cause.cause,
                "rca_confidence": top_cause.confidence,
                "evidence": evidence,
            })

            state.recommendation = result
            logger.info(f"Recommendation completed, is_critical={result.is_critical}")
            return state
        
        except Exception as e:
            attempt += 1
            logger.warning(f"Recommendation attempt {attempt} failed: {e}")
            state.retry_counts["recommendation"] = attempt

    logger.error("Recommendation failed after all retries, marking pipeline degraded")
    state.pipeline_status = "degraded"
    state.failed_stages.append("recommendation")
    state.recommendation = Recommendation(
        actions=[],
        is_critical=True,
        grounded_in=[],
    )
    return state
    

    