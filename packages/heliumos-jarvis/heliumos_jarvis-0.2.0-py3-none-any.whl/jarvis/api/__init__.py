import threading

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from snowflake import SnowflakeGenerator

from jarvis.embeddings.openai import JarvisOpenAIEmbeddings
from jarvis.jarvis_configuration import settings
from jarvis.stores import (
    KnowledgeSourceStore,
    MessageHistoryStore,
    KnowledgeSummaryStore,
    ToolInstanceStore,
    ToolStore,
    MemoryStore
)

llm = ChatOpenAI(
    openai_api_base=f"http://{settings.INFERENCE_MODEL_HOST}:{settings.INFERENCE_MODEL_PORT}/v1",
    openai_api_key="EMPTY",
    model="gpt-3.5-turbo",
    temperature=0.5,
    top_p=0.3,
    default_headers={"x-heliumos-appId": "general-inference"},
    tiktoken_model_name="gpt-3.5-turbo",
    verbose=True,
)
embeddings = JarvisOpenAIEmbeddings(
    openai_api_base=f"http://{settings.EMBEDDING_MODEL_HOST}:{settings.EMBEDDING_MODEL_PORT}/v1",
    openai_api_key="EMPTY",
    default_headers={"x-heliumos-appId": "text-embedding"},
    model="text-embedding-ada-002",
    # chunk_size=512,
    # tiktoken_model_name="text-embedding-ada-002"
)
tool_instance_store = ToolInstanceStore(
    connection_string=f"postgres://"
                      f"{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}"
                      f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
)
tool_store = ToolStore(
    connection_string=f"postgres://"
                      f"{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}"
                      f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
)
knowledge_source_store = KnowledgeSourceStore(
    connection_string=f"postgres://"
                      f"{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}"
                      f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
)
knowledge_summary_store = KnowledgeSummaryStore(
    connection_string=f"postgres://"
                      f"{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}"
                      f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
)

memory_store = MemoryStore(
    connection_string=f"postgres://"
                      f"{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}"
                      f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
)

message_history_store = MessageHistoryStore(
    connection_string=f"postgres://"
                      f"{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}"
                      f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
)

gen = SnowflakeGenerator(2)
lock = threading.Lock()
