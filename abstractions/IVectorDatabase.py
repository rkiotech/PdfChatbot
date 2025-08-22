from abc  import ABC, abstractmethod
from abstractions.IEmbedding import IEmbedding
class IVectorDatabase(ABC):
    @abstractmethod
    def vector_store(self, docs: list,embedding:IEmbedding,collection_name:str,persist_directory:str) -> str:
        """Stores the provided documents in the vector database."""
        pass