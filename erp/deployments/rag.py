import logging
from starlette.requests import Request
# from langchain import hub
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import PromptTemplate
# from langchain_core.runnables import RunnablePassthrough, RunnablePick
from langchain.llms import LlamaCpp
from ray import serve
from erp.components import Ingress
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts.chat import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate
)
from erp.utils import ConfigReader as cr

logger = logging.getLogger("ray.serve")


@serve.deployment
class Rag(Ingress):
    """Main deployment for the Rag app.

    The main deployement is where the compute graph is constructed,
    in this case consisting of 3 deployments, TextSplitter,
    EmbedAndSearch, and Rag. This deployment is also
    the one exposed as an enpoint in the config.yaml file.

    Rag inherits the Ingress class which includes simple request
    reading and validation methods.

    Attributres:
        handles (dict): dict of deployment handles used to create the graph
        config (str): path to Rag deployment config file
        model_path (str): redundant to config but allows coonfigless launch
        n_gpu_layers (str): redundant to config but allows coonfigless launch
        n_batch (int): redundant to config but allows coonfigless launch
        n_ctx (int): redundant to config but allows coonfigless launch
    """
    def __init__(
        self,
        handles: dict,
        config: str = None,
        model_path: str = None,
        n_gpu_layers: str = 1,
        n_batch: int = 512,
        n_ctx: int = 2048,
    ):
        super().__init__()
        # set all values with config if it exists
        if config is not None:
            config_dict = cr.read_config(config)
            self.model_path = config_dict["llm"]["model_path"]
            self.n_gpu_layers = config_dict["llm"]["n_gpu_layers"]
            self.n_batch = config_dict["llm"]["n_batch"]
            self.n_ctx = config_dict["llm"]["n_ctx"]
        else:
            self.model_path = model_path
            self.n_gpu_layers = n_gpu_layers
            self.n_batch = n_batch
            self.n_ctx = n_ctx

        # get the connected deployments
        self.text_splitter = handles["text_splitter"].options(
                use_new_handle_api=True
        )
        self.embed_and_search = handles["embed_and_search"].options(
                use_new_handle_api=True
        )

        # define the llama model from local file
        self.llm = LlamaCpp(
            model_path=self.model_path,
            n_gpu_layers=self.n_gpu_layers,
            n_batch=self.n_batch,
            n_ctx=self.n_ctx,
            f16_kv=True,  # must be set to true
            verbose=False,
        )
        # Get the prompt from a custom created prompt in the Rag config file
        self.rag_prompt = ChatPromptTemplate(
            input_variables=["question", "context"],
            messages=[
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        input_variables=["question", "context"],
                        template=config_dict["rag_prompt"]["template"]
                    )
                )
            ]
        )

        # create the chain
        self.chain = load_qa_chain(
            self.llm,
            chain_type="stuff",
            prompt=self.rag_prompt
        )

    async def __call__(self, request: Request) -> dict:
        """Main method that runs the compute graph

        Args:
            request (starlette.Request): user request to system endpoint

        Returns:
            Response dict from rag process
        """
        request_dict = await self.ingress(request)
        query = request_dict["query"]
        context = request_dict["context"]

        # begin rag process
        text_splits = self.text_splitter.remote(context)
        docs = await self.embed_and_search.remote(
            query,
            text_splits
        )
        llm_answer = self.chain(
            {"input_documents": docs, "question": query}
        )
        answer = llm_answer['output_text']

        logger.info(f'response type: {type(answer)}')
        logger.info(f'response: {answer}')
        response = self.build_response(answer)
        return response

    def build_response(self, answer: str) -> dict:
        """Converts rag response into simple dict to return to user as reponse

        Args:
            answer (str): Rag answer, just the text answer

        Returns:
            Dict simple pickle-able dict for response to user
        """
        response = {}
        response['answer'] = answer
        return response
