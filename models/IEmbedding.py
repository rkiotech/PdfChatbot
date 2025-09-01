from abc import ABC, abstractmethod
class  IEmbedding(ABC):
    def __init__(self):
        self.embedding = None

    def get_embedding(self):
        return self.embedding
    def set_embedding(self, embedding):
        self.embedding = embedding
