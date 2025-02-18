import redis
import logging

class AgentMemory:
    """Stores AI Agent decisions for optimized learning"""

    def __init__(self):
        self.redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

    def store_memory(self, agent_name, key, value):
        """Store AI agent's past actions"""
        try:
            self.redis_client.set(f"{agent_name}:{key}", value)
            logging.info(f"Memory Stored: {agent_name} -> {key} -> {value}")
        except Exception as e:
            logging.error(f"Memory Storage Failed: {e}")

    def retrieve_memory(self, agent_name, key):
        """Retrieve past AI decisions"""
        try:
            return self.redis_client.get(f"{agent_name}:{key}")
        except Exception as e:
            logging.error(f"Memory Retrieval Failed: {e}")
            return None
