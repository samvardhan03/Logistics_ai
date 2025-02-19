import logging
from src.retrieval.keyword_search import BM25Search
from src.retrieval.vector_search import VectorSearch

class HybridSearch:
    """ Combines BM25 (Keyword Search) + FAISS (Vector Search) for better retrieval """

    def __init__(self):
        logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")
        self.bm25_search = BM25Search()
        self.vector_search = VectorSearch()

    def retrieve_documents(self, query_text, top_n=5):
        """ Hybrid search combining BM25 keyword search and FAISS vector search """
        try:
            #Run BM25 keyword-based search
            bm25_results = self.bm25_search.search(query_text, top_n)

            # Run Vector search (Semantic Search)
            vector_results = self.vector_search.search(query_text, top_n)

            # Combine & Rank Results (BM25 + Vector)
            combined_results = self.rank_results(bm25_results, vector_results)
            logging.info(f"Hybrid Search Results: {combined_results}")

            return combined_results

        except Exception as e:
            logging.error(f"Hybrid Search Failed: {e}")
            return None

    def rank_results(self, bm25_results, vector_results):
        """ Merges BM25 & Vector Search results using a ranking function """
        combined = {}

        # Merge BM25 & Vector scores
        for doc in bm25_results:
            combined[doc["id"]] = combined.get(doc["id"], 0) + doc["score"] * 0.6  # BM25 has 60% weight
        for doc in vector_results:
            combined[doc["id"]] = combined.get(doc["id"], 0) + doc["score"] * 0.4  # Vector has 40% weight

        # Sort by highest ranking score
        sorted_results = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        return [{"id": doc_id, "score": score} for doc_id, score in sorted_results]
