import json
class Document():
    page_content: str
    metadata: dict
    def __init__(self, page_content: str, metadata: dict) -> None:
        self.page_content = page_content
        self.metadata = metadata

    def dict(self) -> dict:
        return {
            "page_content": self.page_content,
            "metadata": self.metadata
        }

    def json(self) -> str:
        return json.dumps(self.dict(), ensure_ascii=False)