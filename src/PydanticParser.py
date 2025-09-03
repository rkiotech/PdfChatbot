from abstractions.IParser import IParser

from langchain_core.output_parsers import PydanticOutputParser
class PydanticParser(IParser):
    def __init__(self,parser_obj):
        self.parser_obj=parser_obj
    def get_parser(self):
        
        # self.parser_obj=p
        """Gets the parser from a Pydantic object."""
        return self.parser_obj
        