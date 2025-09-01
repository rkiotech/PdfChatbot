from models.IEmbedding import IEmbedding
from langchain_huggingface import HuggingFaceEmbeddings
class SementicsimEmbedding(IEmbedding):

      def __init__(self):
            self.embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")   
 

