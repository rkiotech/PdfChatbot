from abc import ABC, abstractmethod

class IParser(ABC):
    @abstractmethod
    def get_parser(self, parser_obj) :
        """Gets the parser from a Pydantic object."""
        pass

