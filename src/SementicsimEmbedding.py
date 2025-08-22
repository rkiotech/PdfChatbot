from abstractions.IEmbedding import IEmbedding
from langchain_huggingface import HuggingFaceEmbeddings
class SementicsimEmbedding(IEmbedding):


    def create_embedding(self) -> list:
        """Creates an embedding using the provided embedding model."""
        # embedding=[]
        embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.set_embedding(embedding)

