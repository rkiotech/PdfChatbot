from abc import ABC, abstractmethod
class IUploader(ABC):
    @abstractmethod
    def upload(self, file_path: str) -> str:
        """Uploads a file and returns the URL of the uploaded file."""
        pass
    @abstractmethod
    def load_file(self, file_path: str) -> list:
        """Loads a file and returns its content as a list of IDocElement."""
        pass