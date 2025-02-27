import logging
from pydantic import BaseModel
from typing import List
import rank_bm25
from src.database.keyword_db import get_all_documents

#Define Pydantic Model for Compliance Documents
class ComplianceDocument(BaseModel):
    id: str
    text: str

#Define Pydantic Model for Search Results
class BM25SearchResult(BaseModel):
    id: str
    score: float

class BM25Search:
    """ BM25 Keyword Search for Compliance Documents """

    def __init__(self):
        logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")
        self.documents, self.corpus, self.bm25 = self.load_documents()

    def load_documents(self) -> List[ComplianceDocument]:
        """ Loads all compliance documents into BM25 search model """
        try:
            documents = [ComplianceDocument(**doc) for doc in get_all_documents()]
            corpus = [doc.text.split() for doc in documents]  # Tokenize text
            bm25 = rank_bm25.BM25Okapi(corpus)
            logging.info(f"BM25 Index Loaded with {len(documents)} Documents")
            return documents, corpus, bm25

        except Exception as e:
            logging.error(f"BM25 Index Load Failed: {e}")
            return [], [], None

    def search(self, query_text: str, top_n: int = 5) -> List[BM25SearchResult]:
        """ Searches BM25 index and returns top matching documents """
        try:
            query_tokens = query_text.split()
            scores = self.bm25.get_scores(query_tokens)
            ranked_results = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_n]

            return [BM25SearchResult(id=self.documents[i].id, score=score) for i, score in ranked_results]

        except Exception as e:
            logging.error(f"BM25 Search Failed: {e}")
            return []
