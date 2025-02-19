import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.database.vector_db import get_all_vectors

class VectorSearch:
    """ FAISS / ChromaDB-based Semantic Search """

    def __init__(self):
        logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  #Lightweight transformer model for embeddings
        self.index, self.document_map = self.load_faiss_index()

    def load_faiss_index(self):
        """ Loads FAISS Index with Pre-Encoded Compliance Rules """
        try:
            documents = get_all_vectors()
            embeddings = np.array([doc["vector"] for doc in documents]).astype("float32")
            
            index = faiss.IndexFlatL2(embeddings.shape[1])  #L2 Distance for Nearest Neighbor Search
            index.add(embeddings)

            logging.info(f"FAISS Index Loaded with {len(documents)} Documents")
            return index, {i: doc["id"] for i, doc in enumerate(documents)}

        except Exception as e:
            logging.error(f"FAISS Index Load Failed: {e}")
            return None, {}

    def search(self, query_text, top_n=5):
        """ Searches FAISS for Semantic Matches """
        try:
            query_vector = self.model.encode(query_text).astype("float32")
            distances, indices = self.index.search(np.array([query_vector]), top_n)

            return [{"id": self.document_map[i], "score": 1 - distances[0][j]} for j, i in enumerate(indices[0])]
        
        except Exception as e:
            logging.error(f"FAISS Search Failed: {e}")
            return []
