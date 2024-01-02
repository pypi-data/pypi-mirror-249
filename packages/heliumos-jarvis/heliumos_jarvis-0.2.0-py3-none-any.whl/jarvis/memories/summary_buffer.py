import logging
from typing import Any, Dict, Tuple, Optional
from typing import List

from langchain.memory import ChatMessageHistory
from langchain.memory.summary import SummarizerMixin
from langchain.memory.utils import get_prompt_input_key
from langchain.schema import (
    BaseChatMessageHistory,
)
from langchain.schema import BaseMemory
from langchain.schema.messages import BaseMessage, SystemMessage, get_buffer_string, HumanMessage, AIMessage
from langchain.schema.messages import messages_from_dict, ChatMessage, FunctionMessage
from pydantic import PrivateAttr

from jarvis.stores import MessageHistoryStore

logger = logging.getLogger(__name__)


def _message_from_dict(message: dict) -> BaseMessage:
    _type = message["type"]
    if _type == "human":
        return HumanMessage(**message["data"])
    elif _type == "ai":
        return AIMessage(**message["data"])
    elif _type == "system":
        return SystemMessage(**message["data"])
    elif _type == "chat":
        return ChatMessage(**message["data"])
    elif _type == "function":
        return FunctionMessage(**message["data"])
    else:
        raise ValueError(f"Got unexpected message type: {_type}")


# def messages_from_dict(self, messages: List[dict]) -> List[BaseMessage]:
#     pass
class JarvisSummaryBufferMessageHistory(BaseChatMessageHistory):
    """Chat message history stored in a Postgres database."""

    def __init__(
            self,
            session_id: str,
            history_store: MessageHistoryStore
    ):
        self.session_id = session_id
        self.history_store = history_store

    @property
    def messages(self) -> List[BaseMessage]:  # type: ignore
        """Retrieve the messages from PostgreSQL"""
        items = []
        records = self.history_store.get_history_by_session_id(self.session_id)
        for record in records:
            m = record["message"]
            m["data"]["additional_kwargs"] = {"message_id": record["id"]}
            items.append(m)
        # items = [record["message"] for record in self.cursor.fetchall()]
        # print(items)
        messages = messages_from_dict(items)
        return messages

    def add_message(self, message: BaseMessage) -> None:
        """Append the message to the record in PostgreSQL"""
        self.history_store.add_message(message, self.session_id)

    def remove_message(self, message_id: str) -> None:
        self.history_store.remove_message(message_id)

    def remove_messages(self, message_ids: List[str]) -> None:
        self.history_store.remove_messages(message_ids)

    def clear(self) -> None:
        """Clear session memory from PostgreSQL"""
        # self.history_store.delete_by_session_id(self.session_id)


class JarvisSummaryBufferMemory(BaseMemory, SummarizerMixin):
    """Buffer with summarizer for storing conversation memory."""
    chat_memory: JarvisSummaryBufferMessageHistory = PrivateAttr(default_factory=ChatMessageHistory)
    max_token_limit: int = 2000
    output_key: Optional[str] = None
    input_key: Optional[str] = None
    return_messages: bool = False
    moving_summary_buffer: str = ""
    memory_key: str = "history"

    def __init__(self, message_store, session_id, **kwargs):
        super().__init__(**kwargs)
        self.chat_memory = JarvisSummaryBufferMessageHistory(
            history_store=message_store,
            session_id=session_id
        )

    @property
    def buffer(self) -> List[BaseMessage]:
        return self.chat_memory.messages

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.

        :meta private:
        """
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        #
        if self.return_messages:
            final_buffer: Any = self.buffer
        else:
            final_buffer = get_buffer_string(
                self.buffer, human_prefix=self.human_prefix, ai_prefix=self.ai_prefix
            )
        return {self.memory_key: final_buffer}

    def validate_prompt_input_variables(cls, values: Dict) -> Dict:
        """Validate that prompt input variables are consistent."""
        prompt_variables = values["prompt"].input_variables
        expected_keys = {"summary", "new_lines"}
        if expected_keys != set(prompt_variables):
            raise ValueError(
                "Got unexpected prompt input variables. The prompt expects "
                f"{prompt_variables}, but it should have {expected_keys}."
            )
        return values

    def _get_input_output(
            self, inputs: Dict[str, Any], outputs: Dict[str, str]
    ) -> Tuple[str, str]:
        if self.input_key is None:
            prompt_input_key = get_prompt_input_key(inputs, self.memory_variables)
        else:
            prompt_input_key = self.input_key
        if self.output_key is None:
            if len(outputs) != 1:
                raise ValueError(f"One output key expected, got {outputs.keys()}")
            output_key = list(outputs.keys())[0]
        else:
            output_key = self.output_key
        return inputs[prompt_input_key], outputs[output_key]

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        input_str, output_str = self._get_input_output(inputs, outputs)
        self.chat_memory.add_user_message(input_str)
        self.chat_memory.add_ai_message(output_str)
        self.prune()

    def prune(self) -> None:
        """Prune buffer if it exceeds max token limit"""
        buffer = self.chat_memory.messages
        curr_buffer_length = self.llm.get_num_tokens_from_messages(buffer)
        if curr_buffer_length > self.max_token_limit:
            pruned_memories = []
            while curr_buffer_length > self.max_token_limit:
                pruned_memories.append(buffer.pop(0))
                curr_buffer_length = self.llm.get_num_tokens_from_messages(buffer)
            self.moving_summary_buffer = self.predict_new_summary(
                pruned_memories, self.moving_summary_buffer
            )
            summary_message = SystemMessage(content=self.moving_summary_buffer)
            pruned_memory_ids = [pruned_memory.additional_kwargs["message_id"] for pruned_memory in pruned_memories]
            self.chat_memory.remove_messages(pruned_memory_ids)
            # store summary
            self.chat_memory.add_message(summary_message)

    def clear(self) -> None:
        """Clear memory contents."""
        self.chat_memory.clear()
        self.moving_summary_buffer = ""
