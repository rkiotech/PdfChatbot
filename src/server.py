from fastmcp import FastMCP
import os
import sqlite3
import requests
import random
mcp = FastMCP("RandomServer")

@mcp.tool
def random_number():
    """Generate a random number between 0 and 6."""
    
    return random.randint(0, 6)

@mcp.tool
def special_add(a: int, b: int):
    """Add two numbers together. a and b are integers."""
    return a + b

# @mcp.tool
# def bring_todo_item(id: int):
#     """To fetch an item, use the bring_todo_item tool with the parameter item (integer)."""
#     response=requests.get(f"https://jsonplaceholder.typicode.com/todos/{id}")
#     if response.status_code != 200:
#         return "Item not found."
#     data = response.json()
#     item = data.get("title", "No title found.")
#     return f"Here is your to-do item: {item}"

if __name__ == "__main__":
    mcp.run(transport="stdio")