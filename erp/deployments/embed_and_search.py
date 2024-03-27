import logging
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from ray.serve import deployment

logger = logging.getLogger("ray.serve")


@deployment
class EmbedAndSearch:
    """Prepares text to be used in Qa rag chain

    Embed and search uses embeddings to convert
    split text into vectors, and also performs a
    similartiry search based on the query resturning
    similar documents.

    Note:
        In this simplified version, no embeddings are persisted, and
        no vector database is being used longterm, rather each
        call creates new embeddings used only once per query.
        This project includes the beggings of launching a separate
        db and persisting the embeddings there with the launch_chroma.sh script
        and the ChromaClient deployment.

    Attributes:
        embeddings (LangChainCommunityEmbeddings): Currently SentenceTransformer

    """

    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings()

    def __call__(self, question: str, split_text: list) -> list:
        """Call method runs the main task

        Args:
            question (str): user input question
            split_text (list): result of TextSplitter

        Returns:
            List of similar docs output of vector similarity search
        """
        stored_vectors = self.embedder(split_text)
        documents = self.search(question, stored_vectors)
        return documents

    def embedder(self, split_text: list):
        """Performs text embedding

        Args:
            split_text (list): output of TextSplitter

        Returns:
            Vectorstore object from chroma
        """
        vectorstore = Chroma.from_texts(
            split_text,
            embedding=self.embeddings
        )
        return vectorstore

    def search(self, question: str, vectorstore) -> list:
        """Performs vector similarity search

        Args:
            question (str): User input question
            vectorstore: vector store object

        Returns:
            List of sililar docs to question from vectorstore
        """
        docs = vectorstore.similarity_search(question)
        return docs
