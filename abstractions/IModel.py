from abc import ABC, abstractmethod
class IModel(ABC):
    @abstractmethod
    def invoke(self, content:str,retriver) -> str:
        """Invokes the model with the provided content and returns the response."""

    @abstractmethod
    def get_model(self):
        """Gets the model."""
        pass
    @abstractmethod
    def getContext(self,content:str,retriver) -> str:
        """Returns the context of the model."""
        pass

    @abstractmethod
    def genResponse(self, content: str,context) -> str:
        """Generates a response based on the provided content."""
        pass