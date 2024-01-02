from itertools import islice
from typing import List, Optional, Any, Tuple

from langchain.callbacks.base import Callbacks
from langchain.chains import MapReduceDocumentsChain
from langchain.schema import Document


class BatchedMapReduceDocumentsChain(MapReduceDocumentsChain):
    batch_size: int = 64

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def _chunk_list(self, it: List, limit: int):
        it = iter(it)
        return iter(lambda: list(islice(it, limit)), [])

    async def acombine_docs(
            self,
            docs: List[Document],
            token_max: Optional[int] = None,
            callbacks: Callbacks = None,
            **kwargs: Any,
    ) -> Tuple[str, dict]:
        """Combine documents in a map reduce manner.

        Combine by mapping first chain over all documents, then reducing the results.
        This reducing can be done recursively if needed (if there are many documents).
        """
        batched_docs = self._chunk_list(docs, self.batch_size)
        map_results = []
        for b_docs in batched_docs:
            _map_results = await self.llm_chain.aapply(
                # FYI - this is parallelized and so it is fast.
                [{**{self.document_variable_name: d.page_content}, **kwargs} for d in b_docs],
                callbacks=callbacks,
            )
            map_results.extend(_map_results)
        question_result_key = self.llm_chain.output_key
        result_docs = [
            Document(page_content=r[question_result_key], metadata=docs[i].metadata)
            # This uses metadata from the docs, and the textual results from `results`
            for i, r in enumerate(map_results)
        ]
        result, extra_return_dict = await self.reduce_documents_chain.acombine_docs(
            result_docs, token_max=token_max, callbacks=callbacks, **kwargs
        )
        if self.return_intermediate_steps:
            intermediate_steps = [r[question_result_key] for r in map_results]
            extra_return_dict["intermediate_steps"] = intermediate_steps
        return result, extra_return_dict
