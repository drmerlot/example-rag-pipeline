from langchain_text_splitters import RecursiveCharacterTextSplitter
from ray.serve import deployment


@deployment
class TextSplitter:
    """Prepares text to be embedded"""
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def __call__(self, data: str) -> list:
        """runs the text splitter"""

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=0
        )
        all_splits = text_splitter.split_documents(data)
        return all_splits
