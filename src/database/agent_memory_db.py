import logging
import redis
import json

class AgentMemoryDB:
    """ Stores AI Agent Task Execution Memory (Redis) """

    def __init__(self):
        logging.basicConfig(filename="logs/service_logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def store_memory(self, agent_name, event_id, memory_data):
        """ Stores AI agent memory for future learning """
        key = f"{agent_name}:{event_id}"
        self.redis_client.set(key, json.dumps(memory_data))
        logging.info(f"Memory Stored for {key}")

    def get_memory(self, agent_name, event_id):
        """ Retrieves past memory logs for AI agent """
        key = f"{agent_name}:{event_id}"
        return json.loads(self.redis_client.get(key) or "{}")
