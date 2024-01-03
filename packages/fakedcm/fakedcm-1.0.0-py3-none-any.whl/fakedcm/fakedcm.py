from fake_useragent import UserAgent
import random

class FakeDCM:
    def __init__(self):
        self.user_agent_generator = UserAgent()

    def generate_fake_user_agents(self, num_agents):
        user_agent_list = [self.user_agent_generator.random for _ in range(num_agents)]
        return user_agent_list

    def generate_fake_ips(self, num_ips):
        ip_list = [f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}" for _ in range(num_ips)]
        return ip_list

fake_dcm = FakeDCM()
