

from abstractions.IUploader import IUploader
from langchain_community.document_loaders import PyPDFLoader
class PdfUploader(IUploader):
    def __init__(self):
        self.docs = []
    def load_file(self, file_path: str) -> list:
        """Loads a PDF file and returns its content as a list of IDocElement."""
        try:
           loader = PyPDFLoader(file_path)
           self.docs = loader.load()
           return self.docs
        except Exception as e:
            print(f"Error loading file: {e}")
            return []
    def upload(self, file_path: str) -> str:
        """Uploads a PDF file and returns the URL of the uploaded file."""
        # Here you would implement the logic to upload the PDF file
        # For demonstration purposes, we will return a mock URL
        return f""