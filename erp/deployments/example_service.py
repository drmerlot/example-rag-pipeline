from erp.components import Ingress
from ray import serve


@serve.deployment
class ExampleService(Ingress):
    def __init__(self, handles):
        handles = handles
        pass
