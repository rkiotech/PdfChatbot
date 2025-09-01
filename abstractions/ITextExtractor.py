from abc import ABC, abstractmethod
from models import IDocElement
class ITextExtractor(ABC):
    @abstractmethod
    def extract_text(self, IDocElement) -> list:
        """Extracts text from a file and returns it as list of IDocElement"""
        pass