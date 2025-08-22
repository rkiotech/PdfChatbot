from abstractions.IRetriver import IRetriver
class MmrRetriver (IRetriver):
      def __init__(self):
            self.retriver=None
      def invoke(self, query: str) -> list:
            """Retrieves relevant documents based on the provided query."""
            if self.retriver is None:
                raise ValueError("Retriever is not set. Please set the retriever first.")
            return self.retriver.invoke(query)
      def set_retriver(self,vectorStrore):
            retriver=vectorStrore.as_retriever(    search_type="mmr",
            search_kwargs={
             "k": 3
             })
            self.retriver=retriver
      def get_retriver(self):
            return self.retriver
          
      