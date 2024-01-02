import json
from typing import Optional, Dict, Any

from fastapi import APIRouter
from pydantic import BaseModel

from . import memory_store, gen, message_history_store
from jarvis.exceptions.api_exceptions import JarvisNotFoundException

router = APIRouter()


class MemoryCreation(BaseModel):
    memory_type: str  # BUFFER, SUMMARY_BUFFER, ENTITY, KNOWLEDGE_GRAPH, VECTOR_STORE
    memory_init_params: Optional[Dict[str, Any]] = {}


class MemoryResponse(BaseModel):
    memory_id: str
    memory_type: str  # BUFFER, SUMMARY_BUFFER, ENTITY, KNOWLEDGE_GRAPH, VECTOR_STORE
    memory_init_params: Optional[Dict[str, Any]] = {}


@router.post("/memory")
async def create_memory(request: MemoryCreation):
    memory_id = str(next(gen))
    memory_init_params = json.dumps(request.memory_init_params)
    memory_store.add_memory(
        memory_id,
        request.memory_type,
        memory_init_params
    )
    return MemoryResponse(
        memory_id=memory_id,
        memory_type=request.memory_type,
        memory_init_params=request.memory_init_params
    )


@router.get("/memory/{memory_id}")
async def get_memory_by_id(memory_id: str):
    exists = memory_store.exist_by_id(memory_id)
    if exists is not True:
        raise JarvisNotFoundException(message=f"{memory_id} not found")
    memory = memory_store.get_by_id(memory_id)
    numbers = message_history_store.count_by_session_id(memory_id)
    return {
        "memory_id": memory.id,
        "memory_type": memory.memory_type,
        "memory_init_params": json.loads(memory.memory_init_params),
        "message_amount": numbers
    }


@router.get("/memory/{memory_id}/messages")
async def get_memory_by_id(memory_id: str):
    exists = memory_store.exist_by_id(memory_id)
    if exists is not True:
        raise JarvisNotFoundException(message=f"{memory_id} not found")
    messages = message_history_store.get_history_by_session_id(memory_id)
    return messages


@router.delete("/memory/{id}")
async def deleteMemoryById():
    pass
