import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ray.serve import deployment
from erp.utils import ConfigReader as cr


logger = logging.getLogger("ray.serve")


@deployment
class TextSplitter:
    """Prepares text to be embedded

    Splits context input as preprocessing
    step to embedding.

    Args:
        config (str): config file to set constructor args
        chunk_size (int): text split chunk size, default 25 if no config
        chunk_overlap (int): overlap while splitting, default 5 if no config
    """
    def __init__(
        self,
        config: str = None,
        chunk_size: int = 25,
        chunk_overlap: int = 5
    ):
        if config is not None:
            config_dict = cr.read_config(config)
            self.chunk_size = config_dict["text_splitter"]["chunk_size"]
            self.chunk_overlap = config_dict["text_splitter"]["chunk_overlap"]
        else:
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def __call__(self, data: str) -> list:
        """runs the text splitter

        Args:
            data (str): text data to be split

        Returns:
            list of split docs
        """
        all_splits = self.text_splitter.split_text(data)
        return all_splits
