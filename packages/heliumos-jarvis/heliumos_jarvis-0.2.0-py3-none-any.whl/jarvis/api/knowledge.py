import asyncio
import logging
import time
from typing import (
    Any,
    List, Tuple
)

from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool
from langchain.chains import LLMChain, StuffDocumentsChain, ReduceDocumentsChain
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.schema.vectorstore import VectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus
from pydantic import BaseModel
from pymilvus import Collection
from pymilvus import connections
from pymilvus import utility

from jarvis.chains.map_reduce import BatchedMapReduceDocumentsChain
from jarvis.jarvis_configuration import settings
from jarvis.prompts import SUMMARY_MAP_PROMPT, SUMMARY_COMBINE_PROMPT, TRANSLATE_PROMPT
from jarvis.stores.knowledge_source_store import KnowledgeSummary
# os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:8"
from . import llm, embeddings, knowledge_source_store, knowledge_summary_store, gen
from jarvis.exceptions.api_exceptions import JarvisNotFoundException
from ..chains.reduce import JarvisReduceDocumentsChain
from ..vectorstores.milvus import JarvisMilvus

router = APIRouter()
loop = asyncio.get_event_loop()
ch = logging.StreamHandler()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)


class KnowledgeRequest(BaseModel):
    knowledge_id: str
    source_path: str


class KnowledgeResponse(BaseModel):
    knowledge_id: str
    source_id: str
    source_path: str


def _callback_on_vectorization_completed(future: asyncio.Future):
    source_id = future.result()
    knowledge_source_store.update_knowledge_source(
        source_id=source_id,
        status=99,
    )
    # TODO update the status.


def _callback_on_summary_completed(future: asyncio.Future):
    (summary_id, version, summary) = future.result()
    knowledge_summary_store.update_knowledge_source_summary(
        summary_id=summary_id,
        summary=summary,
        status=99,
        version=version
    )
    summary = knowledge_summary_store.get_by_id(summary_id)
    # send_message("KNOWLEDGE_SOURCE_SUMMARY", summary)


def _load_and_split_document(path: str) -> List[Document]:
    loader = PyPDFLoader(file_path=path)
    input_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=16)
    docs = text_splitter.split_documents(input_documents)
    return docs


# 对文档进行向量化并存储到向量数据库
async def _create_vectorization(source_id: str, vector_store: VectorStore, docs: List[Document]) -> str:
    logger.debug("start vectorization...")
    await run_in_threadpool(vector_store.add_documents, docs)
    logger.debug("end vectorization...")
    return source_id


# 对文档进行总结
async def _summary(summary_id: str, docs: List[Document]) -> Tuple:
    logger.debug("start summary...")
    docs_numbers = len(docs)
    print(docs_numbers)
    batch_size = 4
    if docs_numbers > 32:
        batch_size = 8

    # chain = load_summarize_chain(
    #     llm,
    #     chain_type="map_reduce",
    #     map_prompt=SUMMARY_MAP_PROMPT,
    #     combine_prompt=SUMMARY_COMBINE_PROMPT,
    #     verbose=False,
    # )

    document_prompt = PromptTemplate(
        input_variables=["page_content"],
        template="{page_content}"
    )
    document_variable_name = "text"
    # The prompt here should take as an input variable the
    map_llm_chain = LLMChain(
        llm=llm,
        prompt=SUMMARY_MAP_PROMPT,
        verbose=False
    )
    # We now define how to combine these summaries
    reduce_llm_chain = LLMChain(
        llm=llm,
        prompt=SUMMARY_COMBINE_PROMPT,
        verbose=False,
    )

    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_llm_chain,
        document_prompt=document_prompt,
        document_variable_name=document_variable_name
    )
    # 将map chain生成的docs按照token_max进行分组。每组拼成一个字符串，进行总结。然后判断总的token是否>token_max如果大于继续递归。
    # 如果<token_max 则最后把合成的doc拼起来调用一次总结。
    # TODO 这里可能有机会修改实现进行分组并法总结
    reduce_documents_chain = ReduceDocumentsChain(
        combine_documents_chain=combine_documents_chain,
        token_max=2048,
    )
    chain = BatchedMapReduceDocumentsChain(
        llm_chain=map_llm_chain,
        reduce_documents_chain=reduce_documents_chain,
        batch_size=batch_size,
    )
    start = time.perf_counter()
    result = await chain.arun(input_documents=docs)
    # result = ""
    end = time.perf_counter()
    logger.debug(f"end summary... elapsed {end-start}")
    return summary_id, 0, result


# 对总结的进行翻译
async def _translate(original_str: str) -> str:
    logger.debug("start translate...")
    translate_chain = LLMChain(llm=llm, prompt=TRANSLATE_PROMPT)
    _translated_summary_str = await translate_chain.arun(input=original_str, language="Chinese")
    logger.debug("end translate...")
    return _translated_summary_str


@router.post("/knowledge_source")
async def create_knowledge_source(request: KnowledgeRequest):
    knowledge_id = request.knowledge_id
    try:
        # 判断是否存在
        exists = knowledge_source_store.exist_by_kid_source(request.knowledge_id, request.source_path)
        if exists:
            knowledge = knowledge_source_store.query_by_kid_source(request.knowledge_id, request.source_path)
            return KnowledgeResponse(
                source_id=knowledge.id,
                knowledge_id=knowledge_id,
                source_path=request.source_path,
                status=knowledge.status
            )
        source_id = str(next(gen))
        knowledge_source_store.add_knowledge_source(
            source_id=source_id,
            knowledge_id=knowledge_id,
            source_path=request.source_path,
        )
        source_path = request.source_path
        docs = await run_in_threadpool(lambda: _load_and_split_document(source_path))
        for doc in docs:
            doc.metadata["source_id"] = source_id
            doc.metadata["knowledge_id"] = knowledge_id
        vector_store = JarvisMilvus(
            embedding_function=embeddings,
            collection_name="JARVIS_KNOWLEDGE",
            drop_old=False,
            connection_args={
                "host": settings.MILVUS_HOST,
                "port": settings.MILVUS_PORT,
                "db_name": settings.MILVUS_DB,  # "default",
                "user": settings.MILVUS_USERNAME,  # "cdgouicgkz",
                "password": settings.MILVUS_PASSWORD,  # "YxX777FA0sT2rT4C",
            },
            partition_key="knowledge_id"
        )
        _vectorization_task = asyncio.create_task(
            _create_vectorization(
                source_id,
                vector_store,
                docs))
        _vectorization_task.add_done_callback(_callback_on_vectorization_completed)
        knowledge_source_store.update_knowledge_source(
            source_id=source_id,
            status=1
        )
    finally:
        pass
    return KnowledgeResponse(
        source_id=source_id,
        knowledge_id=knowledge_id,
        source_path=request.source_path,
        status=0
    )


@router.post("/knowledge_source/{knowledge_source_id}/summary")
async def create_source_summary(knowledge_source_id: str) -> None:
    source_record = knowledge_source_store.get_knowledge_source_by_id(knowledge_source_id)
    if source_record is None:
        raise JarvisNotFoundException(f"source_id = {knowledge_source_id} not found")
    exist = knowledge_summary_store.exist_by_source_id(knowledge_source_id)
    if exist:
        return

    source_id = source_record.id
    knowledge_id = source_record.knowledge_id
    source_path = source_record.source_path
    try:
        summary_id = str(next(gen))
        knowledge_summary_store.add_knowledge_source_summary(
            summary_id=summary_id,
            knowledge_id=knowledge_id,
            source_id=source_id,
            summary="",
            status=1
        )
        docs = await run_in_threadpool(lambda: _load_and_split_document(source_path))
        for doc in docs:
            doc.metadata["source_id"] = source_id
        _summary_task = asyncio.create_task(_summary(summary_id, docs))
        _summary_task.add_done_callback(_callback_on_summary_completed)
    finally:
        pass


@router.get("/knowledge_source/{source_id}")
async def get_source_by_id(source_id: str):
    record = knowledge_source_store.get_knowledge_source_by_id(source_id)
    return KnowledgeResponse(
        source_id=record.id,
        knowledge_id=record.knowledge_id,
        source_path=record.source_path
    )


@router.delete("/knowledge_source/{source_id}")
async def delete_knowledge_source_by_id(source_id: str):
    record = knowledge_source_store.get_knowledge_source_by_id(source_id)
    if record is not None:
        knowledge_source_store.delete_by_source_id(source_id)
        connections.connect(
            db_name=settings.MILVUS_DB,
            host=settings.MILVUS_HOST,
            port=settings.MILVUS_PORT,
            user=settings.MILVUS_USERNAME,
            password=settings.MILVUS_PASSWORD,
        )
        collection = Collection(name="JARVIS_KNOWLEDGE")
        res_pks = collection.query(f"source_id == \"{record.id}\" && knowledge_id == \"{record.knowledge_id}\"")
        pks = [m["pk"] for m in res_pks]
        collection.delete(f"pk in {pks}")


@router.delete("/knowledge/{knowledge_id}")
async def delete_knowledge_by_id(knowledge_id: str):
    knowledge_source_store.delete_by_knowledge_id(knowledge_id)
    connections.connect(
        db_name=settings.MILVUS_DB,
        host=settings.MILVUS_HOST,
        port=settings.MILVUS_PORT,
        user=settings.MILVUS_USERNAME,
        password=settings.MILVUS_PASSWORD,
    )
    utility.drop_collection(knowledge_id)


@router.post("/knowledge/{knowledge_id}/answer")
async def generate_answer() -> Any:
    pass


@router.post("/knowledge_source/{knowledge_source_id}/answer")
async def generate_answer() -> Any:
    pass


@router.get("/knowledge_source/{knowledge_source_id}/summary")
async def get_source_summary(knowledge_source_id: str) -> KnowledgeSummary:
    summary = knowledge_summary_store.get_by_source_id(knowledge_source_id)
    return summary
