import logging
from src.retrieval.hybrid_search import hybrid_search
from src.models.compliance_rag import ComplianceRAG

# Load RAG-Based Compliance System
rag_compliance = ComplianceRAG()

class AgenticRAGPipeline:
    """ AI Agentic RAG Pipeline for Compliance Fixes """

    def __init__(self):
        logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")

    def query_compliance_rules(self, query_text):
        """ Fetches Compliance Rules Using Hybrid Search """
        try:
            retrieved_docs = hybrid_search(query_text)
            compliance_fix = rag_compliance.generate_fix(retrieved_docs)
            logging.info(f"Compliance Fix: {compliance_fix}")
            return compliance_fix
        except Exception as e:
            logging.error(f"Compliance Query Failed: {e}")
            return None

