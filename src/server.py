from fastmcp import FastMCP
import os
import sqlite3

import random
mcp = FastMCP("RandomServer")

@mcp.tool
def random_number():
    """Generate a random number between 0 and 6."""
    return random.randint(0, 6)


if __name__ == "__main__":
    mcp.run(transport="stdio")