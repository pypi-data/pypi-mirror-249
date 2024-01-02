from typing import (
    Any,
    Dict,
    Mapping,
    List,
    Optional,

)

from langchain.callbacks.manager import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
)
from langchain.chains import MultiRouteChain
from langchain.chains.base import Chain
from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain
from langchain.chains.router.llm_router import LLMRouterChain


class MultiConversationRetrieveChain(MultiRouteChain):
    """A multi-route chain that uses an LLM router chain to choose amongst retrieval
        qa chains."""

    router_chain: LLMRouterChain
    """Chain for deciding a destination chain and the input to it."""
    destination_chains: Mapping[str, BaseConversationalRetrievalChain]
    """Map of name to candidate chains that inputs can be routed to."""
    default_chain: Chain
    """Default chain to use when router doesn't map input to one of the destinations."""

    @property
    def output_keys(self) -> List[str]:
        return ["result"]

    def _call(
            self,
            inputs: Dict[str, Any],
            run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        callbacks = _run_manager.get_child()
        route = self.router_chain.route(inputs, callbacks=callbacks)
        refined_next_inputs = {**inputs, **route.next_inputs}

        _run_manager.on_text(
            str(route.destination) + ": " + str(refined_next_inputs), verbose=self.verbose
        )
        if not route.destination:

            return self.default_chain(refined_next_inputs, callbacks=callbacks)
        elif route.destination in self.destination_chains:

            return self.destination_chains[route.destination](
                refined_next_inputs, callbacks=callbacks
            )
        elif self.silent_errors:

            return self.default_chain(refined_next_inputs, callbacks=callbacks)
        else:
            raise ValueError(
                f"Received invalid destination chain name '{route.destination}'"
            )

    async def _acall(
            self,
            inputs: Dict[str, Any],
            run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        _run_manager = run_manager or AsyncCallbackManagerForChainRun.get_noop_manager()
        callbacks = _run_manager.get_child()
        route = await self.router_chain.aroute(inputs, callbacks=callbacks)

        refined_next_inputs = {**inputs, **route.next_inputs}
        await _run_manager.on_text(
            str(route.destination) + ": " + str(refined_next_inputs), verbose=self.verbose
        )
        if not route.destination:
            return await self.default_chain.acall(
                refined_next_inputs, callbacks=callbacks
            )
        elif route.destination in self.destination_chains:
            return await self.destination_chains[route.destination].acall(
                refined_next_inputs, callbacks=callbacks
            )
        elif self.silent_errors:
            return await self.default_chain.acall(
                refined_next_inputs, callbacks=callbacks
            )
        else:
            raise ValueError(
                f"Received invalid destination chain name '{route.destination}'"
            )
