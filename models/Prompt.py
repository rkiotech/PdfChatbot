from langchain_core.prompts import PromptTemplate
class Prompt():
    def __init__(self, prompt_text,parser, input_variables):
        self.prompt_text = prompt_text
        self.input_variables = input_variables
        self.template = None
        self.parser = parser

    def get_template(self):
        self.template= PromptTemplate(
        template=f"{self.prompt_text} {{format_instructions}}",
        input_variables=self.input_variables,
        partial_variables={"format_instructions": self.parser.get_format_instructions()})
        return self.template
       

