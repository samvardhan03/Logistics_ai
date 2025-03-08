from fastapi import APIRouter
from src.pipeline.agentic_rag_pipeline import AgenticRAGPipeline

router = APIRouter(tags=["Compliance Automation"])
rag_pipeline = AgenticRAGPipeline()

@router.get("/check")
def check_compliance(query_text: str):
    """ Uses Hybrid Search + RAG to verify compliance rules """
    compliance_results = rag_pipeline.retrieve_compliance_rules({"query_text": query_text})
    return {"query_text": query_text, "compliance_results": compliance_results}
