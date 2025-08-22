from abc import ABC, abstractmethod
from abstractions.IVectorDatabase import IVectorDatabase
class IRetriver(ABC):
    @abstractmethod
    def invoke(self, query: str) -> list:
        """Retrieves relevant documents based on the provided query."""
        pass

    @abstractmethod
    def get_retriver(self,vectorStore) -> str:
        """Returns the retriever."""
        pass