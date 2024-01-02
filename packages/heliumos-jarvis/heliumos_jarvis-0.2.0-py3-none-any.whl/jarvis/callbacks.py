from typing import (
    Any,
    Dict,
    List,
    Optional,
)
from uuid import UUID

from langchain.callbacks.base import BaseCallbackHandler


class JarvisCallBack(BaseCallbackHandler):
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        print(f"""----on chain end:\n {outputs} \n {kwargs}""")

    def on_chain_start(
            self,
            serialized: Dict[str, Any],
            inputs: Dict[str, Any],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
    ) -> None:
        print(f"""----on chain start:\n {inputs} \n {kwargs}""")

    def on_llm_start(
            self,
            serialized: Dict[str, Any],
            prompts: List[str],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
    ) -> None:
        print(f"""----on LLM start:\n {prompts} \n {kwargs}""")
