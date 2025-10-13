import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from langgraph.graph import StateGraph, START, END
from SarvamModel import SarvamModel
from NormalModel import NormalModel
from models.Prompt import Prompt
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from sarvamai import SarvamAI

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_core.messages import AIMessage,HumanMessage
from typing import Literal,Union
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from fastapi import FastAPI
app = FastAPI()

class RandomNumberInput(BaseModel):
    pass

class BringTodoItemInput(BaseModel):
    id: int

class SpecialAddInput(BaseModel):
    a: int
    b: int
class ReadFileInput(BaseModel):
    file_path: str

class GetFilePathInput(BaseModel):
    name: str
global_tool_list=[]
class ToolCall(BaseModel):
     content: str = Field(default="", description="Content from the model")
     tool_called:Literal["True", "False"]=Field( description="Whether a provided tool used or not")
     tool_name:Literal["random_number","bring_todo_item","special_add","read_file","get_file_path"]=Field(default="None", description="Name of the tool used")
     tool_selected: Union[ReadFileInput,SpecialAddInput,BringTodoItemInput,RandomNumberInput,GetFilePathInput] = Field(default=[], description="Description of the tool selected") 
parser=PydanticOutputParser(pydantic_object=ToolCall)
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_id: str=Field(..., example="523")
    tool_called:None
    tools_list:None
    tool_name:None
    tool_selected:None
def sarvam_llm(api_key,prompt):
    # print(type(input),input)
        # print("User input inside model:", user_input)
        # prompt=[{"content": user_input.text, "role": "user"}]
    # print(text)

        client = SarvamAI(
        api_subscription_key=api_key,
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

import json
def convert_messages_to_dict(messages):
    """
    Convert LangChain message objects (HumanMessage, AIMessage)
    into a list of dicts with 'role' and 'content'.
    """
    formatted = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            formatted.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            formatted.append({"role": "assistant", "content": msg.content})
        else:
            # fallback for system or unknown message types
            formatted.append({"role": "system", "content": msg.content})
    return formatted
def chat_node(state: ChatState):
    user_input = state['messages']
    tools_list=state['tools_list']
    # user_input=convert_messages_to_dict(user_input)
    print("User input:", user_input)
    tool_info = [f"ID of tool:{idx} - tool name: {t.name} — tool description: {t.description} — input_schema: {t.inputSchema['properties']}" for idx,t in enumerate(tools_list)]
    tools = "\n".join(tool_info)
    # print("Available tools:", tools)
    # print(user_input)

    # ans=sarvam_llm(api_key="sk_e9hrwjet_SJrtYF4VYTYd474dsVN5Krd4",prompt=user_input)
    # print("Sarvam LLM response:", ans)
    prompt_text= """
You are given these tools:
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

Now answer the following user query using the provided tools if necessary:
{user_input}

"""
    # my_prompt="""give answer {user_input}"""
    # prompt_text= f"Give name of tool that can be possibly use for given user query  tools:{{tools}} user query : {user_input[-1].content}"

    prompt=Prompt(prompt_text,parser=parser,input_variables=["tools","user_input"])
    model=NormalModel(api_key="sk_e9hrwjet_SJrtYF4VYTYd474dsVN5Krd4",prompt=prompt)
    response=model.invoke(user_input=user_input,tools=tools)

    response=response.replace('```json','')
    response=response.replace('```','')

    response=json.loads(response)

    print("Response from model:", response)

    if response['content']!='':
       return {"messages": [user_input[0], AIMessage(content=response['content'])],'tool_selected':response['tool_selected'],'tool_name':response['tool_name']}
    else:
        return {"messages": [user_input[0]],"tool_called":response['tool_called'],'tool_selected':response['tool_selected'],'tool_name':response['tool_name']}


from fastmcp import Client
import asyncio
async def main():

    async with Client("server.py") as client:
        tools = await client.list_tools()

    return tools

def tool_list(state: ChatState):
    tools=asyncio.run(main())
    global_tool_list.clear()
    for t in tools:
        global_tool_list.append({"name":t.name,"description":t.description,"inputSchema":t.inputSchema['properties']})
    return {'tools_list': tools}

def tool_condition(state: ChatState):
    print("Tool condition check:", state.get('tool_called', 'False'))
    if state.get('tool_called', 'False')=='True':
        return 'tool_call'
    else:
        return END
    

async def tool_call_main(state: ChatState):
          async with Client("server.py") as client:
            #    tool_name=state['tool_selected']['name']
            #    inputSchema = {k: v for k, v in state['tool_selected']['inputSchema'].items() if k != 'name'}
            #    print("Invoking tool:", tool_name, "with input schema:", inputSchema)
               result = await client.call_tool(name=state['tool_name'],arguments=state['tool_selected'])
          return result,state['tool_name'],state['tool_selected']


def tool_call(state: ChatState):
    result,tool_name,inputSchema=asyncio.run(tool_call_main(state))
    print("Tool call result:", AIMessage(content=result.content[0].text))
    return {'messages': [AIMessage(content=result.content[0].text,response_metadata={"tool_used": tool_name,"tool_input": inputSchema})]}
graph = StateGraph(ChatState)
graph.add_node('list_tools', tool_list)

graph.add_node("chat_node", chat_node)
graph.add_node("tool_call", tool_call)


graph.add_edge(START, 'list_tools')

graph.add_edge('list_tools', 'chat_node')

graph.add_conditional_edges('chat_node', tool_condition)
graph.add_edge('tool_call', END)

graph.add_edge("chat_node", END)

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)



workflow = graph.compile(checkpointer=checkpointer)
print(workflow)
class QueryId(BaseModel):
      id: str = Field(..., example="1")

class UserInput(BaseModel):
    user_input: str = Field(..., example="what is capital of US?")
    id: str = Field(..., example="1")


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)
@app.post("/invoke/{user_id}")
def invoke_workflow(data: UserInput,user_id: str):
    config = {"configurable": {"thread_id": user_id+"@"+data.id}}

    response=workflow.invoke({'messages':[HumanMessage(content=data.user_input)],'user_id':user_id}, config=config)
    item = response.get('messages', [])
    # print("Final response:", item)
    response['messages'] = item[::-1]  # Reverse the messages list to have the latest message first
    return response
@app.post("/history/{user_id}")
def invoke_workflow(data: QueryId,user_id: str):
    config = {"configurable": {"thread_id":  user_id+"@"+data.id}}

    response=list(workflow.get_state_history(config))
    return response
@app.post("/load_conversation/{user_id}")
def invoke_workflow(data: QueryId,user_id: str):
    config = {"configurable": {"thread_id": user_id+"@"+data.id}}

    state=list(workflow.get_state(config=config))
    return state[0].get('messages',[])
@app.get("/all_threads")
def invoke_workflow():
    threads = retrieve_all_threads()
    return threads



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
