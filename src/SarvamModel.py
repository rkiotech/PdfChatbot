from abstractions.IModel import IModel
from sarvamai import SarvamAI
from MmrRetriver import MmrRetriver
from abstractions.IParser import IParser
from langchain.schema.runnable import RunnableLambda
class SarvamModel(IModel):
    def __init__(self,api_key: str,prompt: str):
        
        self.api_key=api_key
        self.prompt=prompt
        self.model=RunnableLambda(lambda x: self.sarvam_llm(x))
    def invoke(self, content: str,retriver:MmrRetriver) -> str:
        """Invokes the model with the provided content and returns the response."""
        context=self.getContext(content,retriver=retriver)
        
        response=self.genResponse(content,context)
        
        return response
    def sarvam_llm(self,input):
    # print(type(input),input)
        prompt=[{"content": input.text, "role": "user"}]
    # print(text)

        client = SarvamAI(
        api_subscription_key=self.api_key,
        )
        result=client.chat.completions(
        messages=prompt)
   
        result=result.choices[0].message.content
    
        return result
    def get_model(self):
        """Gets the model."""
        if self.model is None:
           self.model = RunnableLambda(lambda x: self.sarvam_llm(x))
        return self.model
    def getContext(self, content: str,retriver:MmrRetriver) -> str:
        """Returns the context of the model."""
        
        # Assuming the model has a method to get context
        return retriver.invoke(content)

    def genResponse(self,content, context) -> str:
        """Generates a response based on the provided content."""
        # Assuming the model has a method to generate response
        template=self.prompt.get_template()
        chain = template | self.model 
        res=chain.invoke({"user_input": content,"context": context})
        return res