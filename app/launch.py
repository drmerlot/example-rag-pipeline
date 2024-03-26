from erp.deployment import ExampleService, Rag
from erp.ConfigReader import read_config

# Read in the app launch config
app_config = read_config('./app_config.yaml')

# deployments with defaults
rag = Rag.bind()

# handles dict:
handles = {
    'rag': rag,  # TODO: this is a placeholder
}

# the main show
response = ExampleService.bind(handles)
