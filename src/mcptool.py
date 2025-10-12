# from dataclasses import Field

import sys,os

from pydantic import BaseModel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
# from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langgraph.prebuilt import ToolNode, tools_condition,create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain.tools import StructuredTool
# from langchain.chat_models import ChatOpenAI
import requests
import random

from NormalModel import NormalModel
from models.Prompt import Prompt
from fastmcp import Client
import asyncio
async def main():
    # Connect via stdio to a local script
    async with Client("server.py") as client:
        
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        result = await client.call_tool("random_number", {})
        print(f"Result: {result.content[0].text}")
if __name__ == "__main__":
    asyncio.run(main())