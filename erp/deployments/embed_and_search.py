import logging
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from ray.serve import deployment

logger = logging.getLogger("ray.serve")


@deployment
class EmbedAndSearch:
    """Prepares text to be used in Qa rag chain"""
    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings()

    def __call__(self, question, split_text) -> tuple:
        stored_vectors = self.embedder(split_text)
        documents = self.search(question, stored_vectors)
        return documents

    def embedder(self, split_text):
        vectorstore = Chroma.from_texts(
            split_text,
            embedding=self.embeddings
        )
        return vectorstore

    def search(self, question, vectorstore):
        docs = vectorstore.similarity_search(question)
        return docs
