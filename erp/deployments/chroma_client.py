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

    def add(self, documents: list, metadatas: list):
        """add to a collection"""
        self.collection.add(
            documents=["This is document1", "This is document2"], # we embed for you, or bring your own
            metadatas=[{"source": "notion"}, {"source": "google-docs"}], # filter on arbitrary metadata!
            ids=["doc1", "doc2"], # must be unique for each doc
        )
        return 0

    def query(self, query_texts: list, n_results: int = 2):
        """Query method on collection defined in init"""
        results = self.collection.query(
            query_texts=query_texts, #["This is a query document"],
            n_results=n_results,
            # where={"metadata_field": "is_equal_to_this"}, # optional filter
            # where_document={"$contains":"search_string"}  # optional filter
        )
        return results
