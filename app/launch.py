from erp.deployments import (
    Rag,
    EmbedAndSearch,
    TextSplitter
)

from erp.utils import ConfigReader as cr

# Read in the app launch config
app_config = cr.read_config('./app_config.yaml')

# deployments with defaults
text_splitter = TextSplitter.bind()
embed_and_search = EmbedAndSearch.bind()

# handles dict:
handles = {
    'text_splitter': text_splitter,
    'embed_and_search': embed_and_search
}

rag = Rag.bind(handles)

# the main show
response = Rag.bind(handles)
