import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.database.db_operations import DatabaseOperations

class VectorDatabase:
    """ FAISS / ChromaDB-Based Vector Search for Compliance Rules """

    def __init__(self):
        logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  
        self.db = DatabaseOperations()
        self.index, self.doc_map = self.load_vector_index()

    def load_vector_index(self):
        """ Loads FAISS index with vector embeddings """
        try:
            rules = self.db.get_all_compliance_rules()
            embeddings = np.array([self.model.encode(rule["text"]).tolist() for rule in rules]).astype("float32")

            index = faiss.IndexFlatL2(embeddings.shape[1])  
            index.add(embeddings)

            logging.info(f"FAISS Index Loaded with {len(rules)} Rules")
            return index, {i: rule["id"] for i, rule in enumerate(rules)}

        except Exception as e:
            logging.error(f"FAISS Index Load Failed: {e}")
            return None, {}

    def search(self, query_text, top_n=5):
        """ Searches FAISS for nearest semantic matches """
        query_vector = self.model.encode(query_text).astype("float32")
        distances, indices = self.index.search(np.array([query_vector]), top_n)

        return [{"id": self.doc_map[i], "score": 1 - distances[0][j]} for j, i in enumerate(indices[0])]
