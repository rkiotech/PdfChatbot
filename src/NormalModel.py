from abstractions.IModel import IModel
from sarvamai import SarvamAI
from MmrRetriver import MmrRetriver
from abstractions.IParser import IParser
from langchain.schema.runnable import RunnableLambda
class NormalModel(IModel):
    def __init__(self,api_key: str,prompt):
        
        self.api_key=api_key
        self.prompt=prompt
        self.model=RunnableLambda(lambda x:self.sarvam_llm(x))
    def invoke(self, content="") -> str:
        """Invokes the model with the provided content and returns the response."""
        # context=self.getContext(content,retriver=retriver)
        template=self.prompt.get_template()
        # print(template)
        chain = template | self.model 

        # chain = self.model 
        response=chain.invoke({"user_input":content})
        
        return response
    def sarvam_llm(self,user_input):
    # print(type(input),input)
      
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
        from langchain.agents import initialize_agent, AgentType
        agent = initialize_agent(
            tools,
            self.model,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
           
        )

        self.model = RunnableLambda(lambda x: agent.invoke(x))
        return self.model
