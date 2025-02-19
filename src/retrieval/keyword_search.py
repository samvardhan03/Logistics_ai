import logging
import rank_bm25
from src.database.keyword_db import get_all_documents

class BM25Search:
    """ BM25 Keyword Search for Compliance Documents """

    def __init__(self):
        logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")
        self.documents, self.corpus, self.bm25 = self.load_documents()

    def load_documents(self):
        """ Loads all compliance documents into BM25 search model """
        try:
            documents = get_all_documents()
            corpus = [doc["text"].split() for doc in documents]  # Tokenize text
            bm25 = rank_bm25.BM25Okapi(corpus)
            logging.info(f"BM25 Index Loaded with {len(documents)} Documents")
            return documents, corpus, bm25

        except Exception as e:
            logging.error(f"BM25 Index Load Failed: {e}")
            return [], [], None

    def search(self, query_text, top_n=5):
        """ Searches BM25 index and returns top matching documents """
        try:
            query_tokens = query_text.split()
            scores = self.bm25.get_scores(query_tokens)
            ranked_results = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_n]

            return [{"id": self.documents[i]["id"], "score": score} for i, score in ranked_results]
        
        except Exception as e:
            logging.error(f"BM25 Search Failed: {e}")
            return []
