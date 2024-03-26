import uuid
import chromadb
from ray.serve import deployment


@deployment
class ChromaClient:
    """Chromadb client

    Deployemnt for interacting with chromadb client

    Attributes:
        client (ChromaDBCleint): client connection to persistant chromadb
        colection (ChromaDBCollection): collection object for adding and querying
    """
    def __init__(self):
        self.client = chromadb.HttpClient()
        self.collection = self.client.create_collection("docs")

    def add(self, documents: list, metadatas: list = None):
        """add to a collection"""
        # generate random UUIDs for each element in docs
        ids = [uuid.uuid4() for x in documents]
        if metadatas is not None:
            self.collection.add(
                documents=documents,  # ["This is document1", "This is document2"]
                metadatas=metadatas,  # [{"source": "notion"}, {"source": "google-docs"}]
                ids=ids  # ["doc1", "doc2"]
            )
        else:
            self.collection.add(
                documents=documents,  # ["This is document1", "This is document2"]
                ids=ids  # ["doc1", "doc2"]
            )
        return 0

    def query(self, query_texts: list, n_results: int = 2):
        """Query method on collection defined in init"""
        results = self.collection.query(
            query_texts=query_texts,  # ["This is a query document"],
            n_results=n_results,
            # where={"metadata_field": "is_equal_to_this"}, # optional filter
            # where_document={"$contains":"search_string"}  # optional filter
        )
        return results
