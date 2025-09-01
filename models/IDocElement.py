class IDocElement():
    def __init__(self, element_type: str, content: str):
        self.element_type = element_type
        self.content = content

    def get_element_type(self) -> str:
        return self.element_type

    def get_content(self) -> str:
        return self.content

    def set_content(self, content: str):
        self.content = content

    def __str__(self) -> str:
        return f"IDocElement(type={self.element_type}, content={self.content})"
    