import redis

class AgentMemory:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def store_memory(self, agent_name, key, value):
        self.redis_client.set(f"{agent_name}:{key}", value)

    def retrieve_memory(self, agent_name, key):
        return self.redis_client.get(f"{agent_name}:{key}")

memory = AgentMemory()
