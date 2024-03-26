from erp.deployments import ExampleService, Rag, ChromaClient
from erp.utils import ConfigReader as cr

# Read in the app launch config
app_config = cr.read_config('./app_config.yaml')

# deployments with defaults
rag = Rag.bind()
chroma_client = ChromaClient.bind()

# handles dict:
handles = {
    'chroma_client': chroma_client,
}

# the main show
response = ExampleService.bind(handles)
