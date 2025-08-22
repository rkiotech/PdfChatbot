from abc import ABC, abstractmethod
class IModel(ABC):

    def invoke(self, content:str,retriver) -> str:
        """Invokes the model with the provided content and returns the response."""
        context=self.getContext(content,retriver=retriver)
        
        response=self.genResponse(content,context)
        return response
       
    @abstractmethod
    def getContext(self,content:str,retriver) -> str:
        """Returns the context of the model."""
        pass

    @abstractmethod
    def genResponse(self, content: str,context) -> str:
        """Generates a response based on the provided content."""
        pass