from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from ray.serve import deployment


@deployment
class EmbedAndSearch:
    """Prepares text to be used in Qa rag chain"""
    def __init__(self):
        self.embedding = GPT4AllEmbeddings()

    def __call__(self, question, split_text) -> tuple:
        stored_vectors = self.embedder(split_text)
        documents = self.search(question, stored_vectors)
        formatted_docs = self.document_formatter(documents)
        return documents, formatted_docs

    def embedder(self, split_text):
        vectorstore = Chroma.from_documents(
            documents=split_text,
            embedding=GPT4AllEmbeddings()
        )
        return vectorstore

    def search(self, question, vectorstore):
        docs = vectorstore.similarity_search(question)
        return docs

    def document_formatter(self, documents):
        """Formats docs for langchain QA chain
        Note:
            directly from -
            https://python.langchain.com/docs/use_cases/question_answering/
                local_retrieval_qa
        """
        return "\n\n".join(doc.page_content for doc in documents)