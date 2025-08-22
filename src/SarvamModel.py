from abstractions.IModel import IModel
from sarvamai import SarvamAI
from MmrRetriver import MmrRetriver
from abstractions.IParser import IParser
from langchain.schema.runnable import RunnableLambda
class SarvamModel(IModel):
    def __init__(self,api_key: str,template ):
        
        self.api_key=api_key
        self.model=template | RunnableLambda( lambda x :self.sarvam_llm(x))
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

    def getContext(self, content: str,retriver:MmrRetriver) -> str:
        """Returns the context of the model."""
        
        # Assuming the model has a method to get context
        return retriver.invoke(content)

    def genResponse(self,content, context) -> str:
        """Generates a response based on the provided content."""
        # Assuming the model has a method to generate response
     

        res=self.model.invoke({"user_input": content,"context": context})
        return res