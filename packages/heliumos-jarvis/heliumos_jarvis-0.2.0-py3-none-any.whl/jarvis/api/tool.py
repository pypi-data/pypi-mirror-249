import json
from typing import (
    Any, Dict, Optional
)

from fastapi import APIRouter
from langchain.chains import LLMMathChain, LLMChain
from langchain.chains import RetrievalQA
from langchain.vectorstores import Milvus
from pydantic import BaseModel

from jarvis.exceptions.api_exceptions import JarvisInternalException
from jarvis.jarvis_configuration import settings
from jarvis.prompts import TRANSLATE_PROMPT
from jarvis.stores.tool_store import ToolInstance
from . import llm, embeddings, tool_store, tool_instance_store, gen

router = APIRouter()


class ToolInstanceCreationRequest(BaseModel):
    tool_id: str
    instance_parameters: Optional[Dict]


class ToolInstanceExecutionRequest(BaseModel):
    input: str


@router.post("/tool_instances")
async def create_tool_instance(request: ToolInstanceCreationRequest) -> Any:
    # TODO query tool
    instance_id = next(gen)
    tool_id = request.tool_id
    tool = tool_store.get_tool_by_id(tool_id)
    instance_parameters = request.instance_parameters
    tool_instance_store.add_tool_instance(
        instance_id=str(instance_id),
        tool_id=tool_id,
        instance_parameters=json.dumps(instance_parameters),
    )
    tool_instance = ToolInstance(
        id=str(instance_id),
        tool_id=tool_id,
        tool_name=tool.tool_name,
        tool_type=tool.tool_type,
        instance_parameters=instance_parameters,
    )
    return tool_instance


@router.get("/tool_instances/{tool_instance_id}")
async def get_tool_instance_by_id(tool_instance_id: str):
    return tool_instance_store.get_instance_by_id(tool_instance_id)


@router.get('/tool_instances')
async def get_tool_instances():
    return tool_instance_store.get_instances()


@router.get("/tools")
async def get_tools():
    return tool_store.get_tools()


@router.get("/tools/{tool_id}")
async def get_tools(tool_id: str):
    return tool_store.get_tool_by_id(tool_id)


@router.post("/tool_instances/{tool_instance_id}/execution")
async def execute_tool_instance(tool_instance_id: str, request: ToolInstanceExecutionRequest):
    instance = tool_instance_store.get_instance_by_id(tool_instance_id)
    if instance.tool_type == "BUILD_IN":
        tool = _load_build_in_tool(instance)
        try:
            output = await tool.arun(request.input)
            return {
                "message": output
            }
        except ValueError as e:
            dd = JarvisInternalException(message=e.args[0])
            raise dd
    else:
        pass


def _load_build_in_tool(tool_instance: ToolInstance) -> LLMChain:
    if tool_instance.tool_name == "MATH":
        chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    elif tool_instance.tool_name == "RETRIEVE":
        knowledge_id = tool_instance.instance_parameters["knowledge_id"]
        vector_store = Milvus(
            embedding_function=embeddings,
            collection_name=knowledge_id,
            connection_args={
                "host": settings.MILVUS_HOST,
                "port": settings.MILVUS_PORT,
                "db_name": settings.MILVUS_DB,  # "default",
                "user": settings.MILVUS_USERNAME,  # "cdgouicgkz",
                "password": settings.MILVUS_PASSWORD,  # "YxX777FA0sT2rT4C",
            }
        )
        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 6,
                "fetch_k": 20
            }
        )

        chain = RetrievalQA.from_chain_type(
            llm=llm,
            verbose=True,
            chain_type="stuff",
            retriever=retriever,

        )
    elif tool_instance.tool_name == "TRANSLATOR":
        language = tool_instance.instance_parameters["language"]
        chain = LLMChain(llm=llm, prompt=TRANSLATE_PROMPT.partial(language=language), verbose=True)
    else:
        chain = LLMChain(llm=llm, verbose=True)
    return chain
