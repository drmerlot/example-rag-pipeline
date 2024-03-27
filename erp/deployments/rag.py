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

        # get the model
        self.llm = LlamaCpp(
            model_path=self.model_path,
            n_gpu_layers=self.n_gpu_layers,
            n_batch=self.n_batch,
            n_ctx=self.n_ctx,
            f16_kv=True,  # must be set to true
            verbose=False,
        )
        # TODO: replace need to pull
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
        response = {}
        response['answer'] = answer
        return response
