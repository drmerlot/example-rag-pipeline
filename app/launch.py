from erp.deployments import (
    Rag,
    EmbedAndSearch,
    TextSplitter
)


# Read in the app launch config
app_config = "./app_config.yaml"

# deployments with defaults
text_splitter = TextSplitter.bind(config=app_config)
embed_and_search = EmbedAndSearch.bind()

# handles dict:
handles = {
    "text_splitter": text_splitter,
    "embed_and_search": embed_and_search
}

# the main show
response = Rag.bind(handles, config=app_config)
