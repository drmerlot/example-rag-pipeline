from starlette.requests import Request
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnablePick
from langchain_community.llms import LlamaCpp
from ray import serve


@serve.deployment
class Rag:
    def __init__(self, handles: dict):
        super().__init__()
        n_gpu_layers = 1  # Metal set to 1 is enough.
        n_batch = 512  # Should be between 1 and n_ctx

        # Make sure the model path is correct for your system!
        self.llm = LlamaCpp(
            model_path="../assets/llama-2-13b.Q4_0.gguf",
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch,
            n_ctx=2048,
            f16_kv=True,  # MUST set to True,
            verbose=True,
        )
        # TODO: replace need to pull
        self.rag_prompt_llama = hub.pull("rlm/rag-prompt-llama")

        self.text_splitter = handles['text_splitter'].options(
                use_new_handle_api=True
        )
        self.embed_and_search = handles['embed_and_search'].options(
                use_new_handle_api=True
        )

    async def __call__(self, request: Request) -> dict:
        request_dict = await self.ingress(request)
        query = request_dict['query']
        context = request_dict['context']

        text_splits = self.text_splitter.remote(context)
        docs, formatted_docs = self.embed_and_search.remote(query, text_splits)

        # run the chain
        chain = (
            RunnablePassthrough.assign(context=RunnablePick("context") | formatted_docs)
            | self.rag_prompt_llama
            | self.llm
            | StrOutputParser()
        )

        response = chain.invoke({"context": docs, "question": query})
        return response
