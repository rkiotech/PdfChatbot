from abc import ABC, abstractmethod
class IModel(ABC):
    @abstractmethod
    def invoke(self, content:str) -> str:
        """Invokes the model with the provided content and returns the response."""


