import Singleton

@Singleton.singleton
class DbManager:
    def __init__(self,vdb,docs,retriver):
        self.vdb=vdb
        self.docs=docs
        self.retriver=retriver
    def get_retriver(self):


        
        vectorStore=self.vdb.vector_store(self.docs)
        print("Documents stored in vector database successfully.")

    
        self.retriver.set_retriver(vectorStore)
        retriver=self.retriver.get_retriver()
        print("Retriever set successfully.")
        return retriver
        
