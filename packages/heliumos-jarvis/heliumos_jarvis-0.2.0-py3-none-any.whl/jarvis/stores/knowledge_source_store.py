import logging
from abc import ABC

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from pydantic import BaseModel

logger = logging.getLogger(__name__)
DEFAULT_CONNECTION_STRING = "postgresql://postgres:mypassword@localhost/q_xun"


class KnowledgeSource(BaseModel):
    knowledge_id: str
    id: str
    source_path: str
    status: int  # 0=INIT 99=FINISHED


class KnowledgeSourceStore(ABC):
    def __init__(
            self,
            connection_string: str = DEFAULT_CONNECTION_STRING,
            table_name: str = "knowledge_source",
    ):
        try:
            self.connection = psycopg.connect(connection_string)
            self.cursor = self.connection.cursor(row_factory=dict_row)
        except psycopg.OperationalError as error:
            logger.error(error)

        self.table_name = table_name

        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        create_table_query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGINT PRIMARY KEY,
            knowledge_id VARCHAR(22),
            source_path TEXT NOT NULL,
            status INT DEFAULT 0,
            version INT DEFAULT 0
        
        );"""
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def add_knowledge_source(self, source_id, knowledge_id, source_path: str):
        query = sql.SQL("INSERT INTO {} (id, knowledge_id, source_path, status) VALUES (%s, %s, %s, %s);").format(
            sql.Identifier(self.table_name)
        )
        self.cursor.execute(
            query, (source_id, knowledge_id, source_path, 0)
        )
        self.connection.commit()

    def update_knowledge_source(
            self,
            source_id: str,
            status: int,
    ):
        query = sql.SQL(
            "UPDATE {} SET status = %s WHERE id = %s;").format(
            sql.Identifier(self.table_name)
        )
        self.cursor.execute(
            query, (status, source_id)
        )
        self.connection.commit()

    def get_knowledge_source_by_id(self, knowledge_id: str) -> KnowledgeSource:
        query = (
            f"SELECT * FROM {self.table_name} WHERE id = %s ORDER by id limit 1 ;"
        )
        self.cursor.execute(query, (knowledge_id,))
        records = self.cursor.fetchall()
        if len(records) > 0:
            return KnowledgeSource(
                id=str(records[0]["id"]),
                knowledge_id=records[0]["knowledge_id"],
                source_path=records[0]["source_path"],
                status=records[0]["status"]
            )
        return None

    def exist_by_kid_source(self, knowledge_id: str, source_path: str) -> bool:
        query = (
            f"SELECT EXISTS (SELECT 1 FROM {self.table_name} WHERE knowledge_id = %s and source_path = %s ) ;"
        )
        self.cursor.execute(query, (knowledge_id, source_path))
        records = self.cursor.fetchall()
        return records[0]['exists']

    def query_by_kid_source(self, knowledge_id: str, source_path: str) -> KnowledgeSource:
        query = (
            f"SELECT * FROM {self.table_name} WHERE knowledge_id = %s and source_path = %s ORDER by id limit 1 ;"
        )
        self.cursor.execute(query, (knowledge_id, source_path))
        records = self.cursor.fetchall()

        return KnowledgeSource(
            id=str(records[0]["id"]),
            knowledge_id=records[0]["knowledge_id"],
            source_path=records[0]["source_path"],
            status=records[0]["status"],
        )

    def delete_by_source_id(self, source_id: str):
        query = f"DELETE FROM {self.table_name} WHERE id = %s;"
        self.cursor.execute(query, (source_id,))
        self.connection.commit()

    def delete_by_knowledge_id(self, knowledge_id: str):
        query = f"DELETE FROM {self.table_name} WHERE knowledge_id = %s;"
        self.cursor.execute(query, (knowledge_id,))
        self.connection.commit()


class KnowledgeSummary(BaseModel):
    id: str
    knowledge_id: str
    knowledge_source_id: str
    summary: str
    status: int


class KnowledgeSummaryStore(ABC):
    def __init__(
            self,
            connection_string: str = DEFAULT_CONNECTION_STRING,
            table_name: str = "knowledge_summary",
    ):
        try:
            self.connection = psycopg.connect(connection_string)
            self.cursor = self.connection.cursor(row_factory=dict_row)
        except psycopg.OperationalError as error:
            logger.error(error)

        self.table_name = table_name

        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        create_table_query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGINT PRIMARY KEY,
            knowledge_id VARCHAR(22),
            source_id BIGINT,
            summary TEXT,
            status INT DEFAULT 0,
            version INT DEFAULT 0 
        );"""
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def add_knowledge_source_summary(
            self,
            summary_id: str,
            knowledge_id: str,
            source_id: str,
            summary: str,
            status: int,
    ):
        query = sql.SQL(
            "INSERT INTO {} (id, knowledge_id, source_id, summary, status, version) VALUES (%s, %s, %s, %s, %s, 0);").format(
            sql.Identifier(self.table_name)
        )
        self.cursor.execute(
            query, (summary_id, knowledge_id, source_id, summary, status)
        )
        self.connection.commit()

    def update_knowledge_source_summary(
            self,
            summary_id: str,
            summary: str,
            status: int,
            version: int,
    ):
        query = sql.SQL(
            "UPDATE {} SET summary = %s, status = %s, version = %s WHERE id = %s and version = %s;").format(
            sql.Identifier(self.table_name)
        )
        self.cursor.execute(
            query, (summary, status, version + 1, summary_id, version)
        )
        self.connection.commit()

    def exist_by_source_id(self, source_id: str) -> bool:
        query = (
            f"SELECT EXISTS (SELECT 1 FROM {self.table_name} WHERE source_id = %s ) ;"
        )
        self.cursor.execute(query, (source_id,))
        records = self.cursor.fetchall()
        return records[0]['exists']

    def get_by_id(self, summary_id):
        query = (
            f"SELECT * FROM {self.table_name} WHERE id = %s ORDER by id limit 1 ;"
        )
        self.cursor.execute(query, (summary_id,))
        records = self.cursor.fetchall()

        return KnowledgeSummary(
            id=str(records[0]["id"]),
            knowledge_id=records[0]["knowledge_id"],
            knowledge_source_id=str(records[0]["source_id"]),
            summary=records[0]["summary"],
            status=records[0]["status"],

        )

    def get_by_source_id(
            self,
            knowledge_source_id: str
    ):
        query = (
            f"SELECT * FROM {self.table_name} WHERE source_id = %s ORDER by id limit 1 ;"
        )
        self.cursor.execute(query, (knowledge_source_id,))
        records = self.cursor.fetchall()

        return KnowledgeSummary(
            id=str(records[0]["id"]),
            knowledge_id=records[0]["knowledge_id"],
            knowledge_source_id=str(records[0]["source_id"]),
            summary=records[0]["summary"],
            status=records[0]["status"],

        )
