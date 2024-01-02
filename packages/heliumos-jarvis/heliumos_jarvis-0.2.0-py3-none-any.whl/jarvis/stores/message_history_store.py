import json
import logging
from abc import ABC
from typing import List

from langchain.schema.messages import BaseMessage, _message_to_dict

logger = logging.getLogger(__name__)

DEFAULT_CONNECTION_STRING = "postgresql://postgres:mypassword@localhost/chat_history"


class MessageHistoryStore(ABC):
    def __init__(
            self,
            connection_string: str = DEFAULT_CONNECTION_STRING,
            table_name: str = "message_history_store",
    ):
        import psycopg
        from psycopg.rows import dict_row

        try:
            self.connection = psycopg.connect(connection_string)
            self.cursor = self.connection.cursor(row_factory=dict_row)
        except psycopg.OperationalError as error:
            logger.error(error)

        self.table_name = table_name

        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        create_table_query = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
               id SERIAL PRIMARY KEY,
               session_id TEXT NOT NULL,
               message JSONB NOT NULL
           );"""
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def get_history_by_session_id(self, session_id):
        query = (
            f"SELECT id, message FROM {self.table_name} WHERE session_id = %s ORDER BY id;"
        )
        self.cursor.execute(query, (session_id,))
        return self.cursor.fetchall()

    def add_message(self, message: BaseMessage, session_id: str) -> None:
        """Append the message to the record in PostgreSQL"""
        from psycopg import sql

        query = sql.SQL("INSERT INTO {} (session_id, message) VALUES (%s, %s);").format(
            sql.Identifier(self.table_name)
        )
        self.cursor.execute(
            query, (session_id, json.dumps(_message_to_dict(message)))
        )
        self.connection.commit()

    def remove_message(self, message_id: str) -> None:
        query = f"DELETE FROM {self.table_name} WHERE id = %s;"
        self.cursor.execute(query, (message_id))
        self.connection.commit()

    def remove_messages(self, message_ids: List[str]) -> None:
        query = f"DELETE FROM {self.table_name} WHERE id = %s;"
        for message_id in message_ids:
            self.cursor.execute(query, (message_id,))
        self.connection.commit()

    def delete_by_session_id(self, session_id):
        query = f"DELETE FROM {self.table_name} WHERE session_id = %s;"
        self.cursor.execute(query, (session_id,))
        self.connection.commit()

    def count_by_session_id(self, session_id) -> int:
        query = (
            f"SELECT COUNT(id) FROM {self.table_name} WHERE session_id = %s LIMIT 1;"
        )
        self.cursor.execute(query, (session_id,))
        counts = self.cursor.fetchall()
        return counts[0]
