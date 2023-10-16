import random
import torch

class ReplayMemory():
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0
    
    def insert(self, transition):
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = transition
        self.position = (self.position + 1) % self.capacity

    def can_sample(self, batch_size):
        return len(self.memory) >= batch_size * 10
    
    def sample(self, batch_size):
        assert self.can_sample(batch_size)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        transitions = random.sample(self.memory, batch_size)
        batch = zip(*transitions)
        return  [torch.cat([item.to(device) for item in items]) for items in batch]
    
