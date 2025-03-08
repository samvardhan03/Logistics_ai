import logging
import rank_bm25
from src.database.db_operations import DatabaseOperations

class BM25Index:
    """ BM25 Index for Fast Compliance Rule Retrieval """

    def __init__(self):
        logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")
        self.db = DatabaseOperations()
        self.rules, self.corpus, self.bm25 = self.load_index()

    def load_index(self):
        """ Loads compliance rules into BM25 model """
        try:
            rules = self.db.get_all_compliance_rules()
            corpus = [rule["text"].split() for rule in rules]
            bm25 = rank_bm25.BM25Okapi(corpus)
            logging.info(f"BM25 Index Loaded with {len(rules)} Rules")
            return rules, corpus, bm25

        except Exception as e:
            logging.error(f"BM25 Index Load Failed: {e}")
            return [], [], None

    def search(self, query_text, top_n=5):
        """ Retrieves top compliance rules based on keyword similarity """
        query_tokens = query_text.split()
        scores = self.bm25.get_scores(query_tokens)
        ranked_results = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_n]

        return [{"id": self.rules[i]["id"], "score": score} for i, score in ranked_results]
