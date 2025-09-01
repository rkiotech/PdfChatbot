from abstractions.IVectorDatabase import IVectorDatabase

from langchain_community.vectorstores import Chroma
class ChromaVectordb(IVectorDatabase):
    def __init__(self, embedding, collection_name, persist_directory):
        self.embedding = embedding
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.store = None

    def vector_store(self, docs):
        """Stores the provided documents in the vector database."""
        
        self.store=Chroma.from_documents(
          documents=docs,
          collection_name=self.collection_name,
          embedding=self.embedding.get_embedding(),
          persist_directory=self.persist_directory,
        )
        return self.store
