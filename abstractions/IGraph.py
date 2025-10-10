from langgraph.graph import StateGraph, START, END

class IGraph:
    def __init__(self):
        self.graph = StateGraph()
    
    def add_node(self, name: str, func):
        self.graph.add_node(name, func)
    
    def add_edge(self, from_node: str, to_node: str):
        self.graph.add_edge(from_node, to_node)
    
    def compile(self, checkpointer=None):
        return self.graph.compile(checkpointer=checkpointer)