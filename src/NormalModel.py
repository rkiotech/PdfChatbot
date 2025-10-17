from abstractions.IModel import IModel
from models.Prompt import Prompt
from sarvamai import SarvamAI
from MmrRetriver import MmrRetriver
from abstractions.IParser import IParser
from langchain.schema.runnable import RunnableLambda
class NormalModel(IModel):
    def __init__(self,api_key):
        
        self.api_key=api_key
        self.prompt_text=""
        self.prompt=None
        self.tools=None
        self.model=RunnableLambda(lambda x:self.sarvam_llm(x))
    def set_prompt(self,prompt_text:str,parser:IParser):
        self.prompt_text=self.prompt_text+prompt_text
        self.parser=parser
    def invoke(self, user_input,context="",history="") -> str:
        """Invokes the model with the provided content and returns the response."""
        # context=self.getContext(content,retriver=retriver)
      
        # print("prompt text",self.prompt_text)
        self.prompt=Prompt(self.prompt_text,parser=self.parser,input_variables=["user_input","context","tools","history"])
        template=self.prompt.get_template()
        # print(template)
        chain = template | self.model 
        # print("Prompt template:", template)
        # print("Content passed to model:", user_input)
        # chain = self.model 
        response=chain.invoke({"user_input":user_input,"context":context,"tools":self.tools,"history":history})
        
        return response
    def sarvam_llm(self,user_input):
    # print(type(input),input)
        print("User input inside model:", user_input)
        prompt=[{"content": user_input.text, "role": "user"}]
    # print(text)

        client = SarvamAI(
        api_subscription_key=self.api_key,
        )
        # client.chat.completions()
        # output=client.chat.completions(
        #     stream=True,
        # messages=prompt)
        result=client.chat.completions(
            
        messages=prompt)
        
        # print("************",output)
        result=result.choices[0].message.content
    
        return result
    def bind_tools(self, tools):
        """Binds tools to the model."""
        self.tools=tools
  
        item= """\n You are given these tools:
    {tools}

Each tool has a specific input schema. 
When you output your result, make sure your "input_schema" strictly follows the tool's defined schema. 
Do not create new keys or arrays.
RULE:
if use same variable name that mentions in input schema of tool.
if the user query is not related to any tool then do not call any tool and give answer
If thier is required to call multiple tools then call respectively to provide answer
Retrive file path if user want to read file
Read file at given path and give content of file if user give path of file
"""
        self.prompt_text=self.prompt_text+item
        return self
       
